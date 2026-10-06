"""LLM judge: scores an agent's answer against the computed ground truth."""
import json
import os

import re

from agent import DEFAULT_MODEL, FALLBACK_KWARGS, OLLAMA, make_client

JUDGE_MODEL = os.environ.get("JUDGE_MODEL", DEFAULT_MODEL if OLLAMA else "claude-opus-5-5")

SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "integer", "description": "0-100: how much of the ground truth the answer gets right"},
        "verdict": {"type": "string", "enum": ["correct", "partially_correct", "incorrect"]},
        "correct_points": {"type": "array", "items": {"type": "string"}},
        "missed_or_wrong": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string", "description": "one or two sentences"},
    },
    "required": ["score", "verdict", "correct_points", "missed_or_wrong", "summary"],
    "additionalProperties": False,
}

PROMPT = """You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
{question}

GROUND TRUTH (authoritative, computed from the data):
{truth}

STRUCTURED FACTS:
{facts}

ANALYST'S ANSWER:
{answer}

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed)."""


async def grade(question: str, truth: str, facts: dict, answer: str) -> dict:
    if not answer.strip():
        return {"score": 0, "verdict": "incorrect", "correct_points": [], "missed_or_wrong": ["no answer"],
                "summary": "The agent produced no answer."}
    content = PROMPT.format(question=question, truth=truth, facts=json.dumps(facts, default=str), answer=answer)
    if OLLAMA:  # no structured-output support: ask for the schema in the prompt and parse leniently
        content += ("\n\nRespond with only a JSON object (no prose, no code fence) matching this JSON schema:\n"
                    + json.dumps(SCHEMA))
        extra = {}
    else:
        extra = {"output_config": {"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}}}
    resp = await make_client().beta.messages.create(
        model=JUDGE_MODEL,
        max_tokens=16000 if OLLAMA else 4000,  # leave room for the local model's thinking
        messages=[{"role": "user", "content": content}],
        **extra,
        **FALLBACK_KWARGS,
    )
    if resp.stop_reason == "refusal":
        return {"score": 0, "verdict": "incorrect", "correct_points": [], "missed_or_wrong": ["judge refused"],
                "summary": "Judge declined to grade."}
    text = "\n".join(b.text for b in resp.content if b.type == "text")
    return parse_grade(text)


def parse_grade(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    try:
        g = json.loads(m.group(0) if m else text)
    except json.JSONDecodeError:
        return {"score": 0, "verdict": "incorrect", "correct_points": [], "missed_or_wrong": ["judge output unparseable"],
                "summary": text.strip()[:300] or "Judge returned no text."}
    g.setdefault("correct_points", [])
    g.setdefault("missed_or_wrong", [])
    g.setdefault("summary", "")
    g.setdefault("verdict", "incorrect")
    g["score"] = int(g.get("score", 0))
    return g
