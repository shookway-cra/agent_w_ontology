"""The analyst agent: Claude + MCP tools, with the ontology server switchable on/off.

Both configurations use the identical model, system prompt, simdb MCP server and
loop. The only difference is whether the `ontology` MCP server (SPARQL) is attached.
"""
import asyncio
import json
import os
import sys
import time
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from pathlib import Path

import anthropic
from mcp import Client, StdioServerParameters

ROOT = Path(__file__).resolve().parent.parent
# DEMO_PROVIDER=ollama runs against a local Ollama server via its Anthropic-compatible API.
PROVIDER = os.environ.get("DEMO_PROVIDER", "anthropic").lower()
OLLAMA = PROVIDER == "ollama"
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("DEMO_MODEL", "qwen3:30b" if OLLAMA else "claude-opus-5-5")
# Local models have much smaller context windows, so keep tool results shorter.
MAX_TOOL_RESULT_CHARS = int(os.environ.get("MAX_TOOL_RESULT_CHARS", 12000 if OLLAMA else 40000))
# Server-side refusal fallback (on by default, Anthropic only). Set DEMO_FALLBACKS=0 to send plain requests.
FALLBACK_KWARGS = ({} if OLLAMA or os.environ.get("DEMO_FALLBACKS", "1") == "0"
                   else {"betas": ["server-side-fallback-2026-07-01"], "fallbacks": "default"})


def make_client() -> anthropic.AsyncAnthropic:
    if OLLAMA:  # Ollama ignores the key but the SDK requires one
        return anthropic.AsyncAnthropic(base_url=OLLAMA_URL, api_key="ollama", timeout=1800)
    return anthropic.AsyncAnthropic()

SYSTEM_PROMPT = """\
You are a military operations-research analyst answering questions about the output of an AFSIM \
simulation run. Use the tools provided to ground every number in data - query rather than guess, \
and enumerate what you counted. When you need to classify weapons, platforms or units, use \
authoritative data from your tools wherever it is available; if you fall back on your own \
background knowledge for a classification, say so explicitly.

Finish with a concise final answer: the headline numbers first, then the breakdown, then any \
assumptions or uncertainties."""

# Extra guidance for local models, which tend to answer after one or two queries.
LOCAL_MODEL_GUIDANCE = """\
# Working method
Work in steps and expect to make 5-10 tool calls before answering. Never answer from schema or overview output alone.
1. Classify first. Before counting, establish exactly which items belong to each category in the question \
(weapon class, unit echelon or hierarchy, nation, equipment role, side). If an ontology tool is available, look \
each category up there and list all its members, including subclasses and aliases. Do not classify from names \
or designations.
2. When the ontology and your background knowledge disagree, follow the ontology.
3. Count with SQL restricted to exactly those members, and confirm which side each platform or weapon belongs to.
4. An empty result or an error is not evidence that nothing exists. Try at least two other queries (broader \
filters, alternative names or properties) before concluding that.
5. Before answering, run one more query that checks your result, e.g. that the breakdown sums to the total."""


def server_params(name: str) -> StdioServerParameters:
    env = {**os.environ, "PYTHONUTF8": "1"}
    script = {"simdb": "simdb_server.py", "ontology": "ontology_server.py"}[name]
    return StdioServerParameters(command=sys.executable, args=[str(ROOT / "mcp_servers" / script)], env=env,
                                 cwd=str(ROOT))


@dataclass
class ToolCall:
    name: str
    input: dict
    output: str
    seconds: float
    is_error: bool = False


@dataclass
class AgentResult:
    mode: str
    question: str
    answer: str = ""
    tool_calls: list = field(default_factory=list)
    turns: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    seconds: float = 0.0
    model_seconds: float = 0.0  # time spent waiting on the model, summed over turns
    stop_reason: str = ""
    error: str | None = None

    def to_dict(self):
        d = dict(self.__dict__)
        d["tool_calls"] = [tc.__dict__ for tc in self.tool_calls]
        return d


async def run_agent(question: str, use_ontology: bool, model: str = DEFAULT_MODEL, effort: str = "high",
                    max_turns: int = 40, on_event=None) -> AgentResult:
    mode = "ontology ON" if use_ontology else "ontology OFF"
    result = AgentResult(mode=mode, question=question)
    emit = on_event or (lambda *_: None)
    t0 = time.time()
    client = make_client()
    # Anthropic-only request options; Ollama models think by default.
    extra = {} if OLLAMA else {"thinking": {"type": "adaptive"}, "output_config": {"effort": effort}}

    async with AsyncExitStack() as stack:
        servers = ["simdb"] + (["ontology"] if use_ontology else [])
        mcp_clients, tools, routes, instructions = {}, [], {}, []
        for name in servers:
            c = await stack.enter_async_context(Client(server_params(name)))
            mcp_clients[name] = c
            if c.instructions:
                instructions.append(f"## MCP server: {name}\n{c.instructions}")
            for t in (await c.list_tools()).tools:
                qualified = f"{name}__{t.name}"
                routes[qualified] = (name, t.name)
                tools.append({"name": qualified, "description": t.description or "",
                              "input_schema": t.input_schema})

        system = (SYSTEM_PROMPT + ("\n\n" + LOCAL_MODEL_GUIDANCE if OLLAMA else "")
                  + "\n\n# Connected data sources\n\n" + "\n\n".join(instructions))
        messages = [{"role": "user", "content": question}]

        async def call(block):
            st = time.time()
            try:
                if block.name not in routes:  # hallucinated tool name: tell the model rather than crash
                    raise KeyError(f"no tool named {block.name!r}; available: {', '.join(sorted(routes))}")
                server, tool = routes[block.name]
                r = await mcp_clients[server].call_tool(tool, block.input)
                text = "".join(getattr(b, "text", "") for b in r.content) or "(empty result)"
                is_err = bool(getattr(r, "is_error", False))
            except Exception as e:  # surface tool failures to the model rather than crashing
                text, is_err = f"Tool error: {e}", True
            if len(text) > MAX_TOOL_RESULT_CHARS:
                text = text[:MAX_TOOL_RESULT_CHARS] + "\n... [truncated]"
            tc = ToolCall(block.name, block.input, text, round(time.time() - st, 2), is_err)
            result.tool_calls.append(tc)
            emit(mode, "tool", tc)
            return {"type": "tool_result", "tool_use_id": block.id, "content": text, "is_error": is_err}

        nudged = False
        try:
            while result.turns < max_turns:
                result.turns += 1
                mt = time.time()
                resp = await client.beta.messages.create(
                    model=model,
                    max_tokens=16000,
                    system=system,
                    tools=tools,
                    messages=messages,
                    **extra,
                    **FALLBACK_KWARGS,
                )
                result.model_seconds += time.time() - mt
                result.input_tokens += resp.usage.input_tokens or 0
                result.output_tokens += resp.usage.output_tokens or 0
                result.cache_read_tokens += getattr(resp.usage, "cache_read_input_tokens", 0) or 0
                result.stop_reason = resp.stop_reason
                messages.append({"role": "assistant", "content": resp.content})
                for b in resp.content:
                    if b.type == "text" and b.text.strip():
                        emit(mode, "text", b.text)

                if resp.stop_reason == "refusal":
                    result.error = "model refused the request"
                    break
                if resp.stop_reason == "pause_turn":
                    continue
                if resp.stop_reason != "tool_use":
                    result.answer = "\n".join(b.text for b in resp.content if b.type == "text").strip()
                    if not result.answer and not nudged:  # ended without an answer: ask once for it
                        nudged = True
                        messages.append({"role": "user", "content": "You ended without giving an answer. Give your "
                                         "final answer now from what you have found, stating any uncertainty."})
                        continue
                    break
                tool_blocks = [b for b in resp.content if b.type == "tool_use"]
                tool_results = await asyncio.gather(*(call(b) for b in tool_blocks))
                messages.append({"role": "user", "content": list(tool_results)})
            else:
                result.error = f"stopped after {max_turns} turns"
        except anthropic.APIError as e:
            result.error = f"{type(e).__name__}: {e}"

    result.seconds = round(time.time() - t0, 1)
    result.model_seconds = round(result.model_seconds, 1)
    return result


def summarize_call(tc: ToolCall, width=110) -> str:
    arg = tc.input.get("query") or tc.input.get("text") or (json.dumps(tc.input) if tc.input else "")
    arg = " ".join(str(arg).split())
    if len(arg) > width:
        arg = arg[: width - 3] + "..."
    return f"{tc.name}({arg})" + ("  [ERROR]" if tc.is_error else "")
