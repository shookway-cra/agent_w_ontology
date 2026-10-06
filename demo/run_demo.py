"""Run the ontology vs no-ontology comparison.

Examples
  python demo/run_demo.py --list
  python demo/run_demo.py q1                       # both modes side by side, judged
  python demo/run_demo.py q2 q3 --ontology off     # baseline only
  python demo/run_demo.py --all
  python demo/run_demo.py --ask "Which Red units fired Lancets?" --ontology both

Each run writes runs/<timestamp>/report.md and results.json.
"""
import argparse
import asyncio
import json
import os
import subprocess
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).parent))
from agent import DEFAULT_MODEL, OLLAMA, run_agent, summarize_call  # noqa: E402
from judge import grade  # noqa: E402
from questions import BY_ID, KB, QUESTIONS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = os.environ.get("SPARQL_ENDPOINT", "http://127.0.0.1:3030/battlespace/sparql")
COLOR = {"ontology ON": "\033[92m", "ontology OFF": "\033[93m"}
RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"


def endpoint_up() -> bool:
    try:
        return httpx.get(ENDPOINT, timeout=2).status_code == 200
    except httpx.HTTPError:
        return False


def ensure_endpoint():
    """Start the bundled SPARQL endpoint if nothing is listening. Returns the process (or None)."""
    if endpoint_up():
        return None
    print(f"{DIM}starting SPARQL endpoint at {ENDPOINT} ...{RESET}")
    proc = subprocess.Popen([sys.executable, str(ROOT / "ontology" / "sparql_server.py")],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(240):  # loading includes the OWL-RL closure
        if endpoint_up():
            return proc
        time.sleep(0.5)
    proc.terminate()
    raise SystemExit("SPARQL endpoint did not start")


def live(mode, kind, payload):
    c = COLOR.get(mode, "")
    if kind == "tool":
        print(f"{c}[{mode:>12}]{RESET} {DIM}->{RESET} {summarize_call(payload)}")


async def run_question(qid, prompt, modes, model, effort, judge, kb):
    q = BY_ID.get(qid)
    print(f"\n{BOLD}=== {qid}: {q.title if q else 'ad-hoc question'} ==={RESET}  {DIM}started "
          f"{datetime.now():%H:%M:%S}{RESET}\n{textwrap.fill(prompt, 100)}\n")
    t0 = time.time()
    if OLLAMA:  # a local server handles one request at a time; run modes in turn so each mode's timing is its own
        results = [await run_agent(prompt, m, model=model, effort=effort, on_event=live) for m in modes]
    else:
        results = await asyncio.gather(*(run_agent(prompt, m, model=model, effort=effort, on_event=live)
                                         for m in modes))
    truth, facts = q.ground_truth(kb) if q else (None, None)
    grades, judge_seconds = {}, 0.0
    if judge and q:
        jt = time.time()
        gl = await asyncio.gather(*(grade(prompt, truth, facts, r.answer) for r in results))
        grades = {r.mode: g for r, g in zip(results, gl)}
        judge_seconds = round(time.time() - jt, 1)
    wall = round(time.time() - t0, 1)

    for r in results:
        c = COLOR.get(r.mode, "")
        print(f"\n{c}{BOLD}--- {r.mode} ---{RESET}  {len(r.tool_calls)} tool calls, {r.turns} turns, "
              f"{fmt_s(r.seconds)} (model {fmt_s(r.model_seconds)}), "
              f"{r.input_tokens:,} in / {r.output_tokens:,} out tokens")
        if r.error:
            print(f"ERROR: {r.error}")
        print(r.answer)
        if r.mode in grades:
            g = grades[r.mode]
            print(f"{c}{BOLD}JUDGE: {g['score']}/100 ({g['verdict']}){RESET} - {g['summary']}")
            for m in g["missed_or_wrong"]:
                print(f"   x {m}")
    if truth:
        print(f"\n{BOLD}GROUND TRUTH:{RESET} {textwrap.fill(truth, 110, subsequent_indent='  ')}")
    print(f"{DIM}{qid} finished in {fmt_s(wall)}" + (f" (judge {fmt_s(judge_seconds)})" if grades else "") + RESET)
    return {"id": qid, "title": q.title if q else "ad-hoc", "prompt": prompt,
            "why_ontology_helps": q.why_ontology_helps if q else None,
            "ground_truth": truth, "results": [r.to_dict() for r in results], "grades": grades,
            "seconds": wall, "judge_seconds": judge_seconds}


def fmt_s(s: float) -> str:
    s = int(round(s))
    return f"{s // 3600}h{s % 3600 // 60:02d}m{s % 60:02d}s" if s >= 3600 else f"{s // 60}m{s % 60:02d}s"


def stats_tables(runs, total_seconds) -> list[str]:
    """Markdown timing summary: one row per question/mode, then per-mode aggregates."""
    rows = ["| Question | Mode | Agent time | Model time | Tool time | Turns | Tool calls | Slowest tool call "
            "| Output tokens | Score |", "|---|---|---|---|---|---|---|---|---|---|"]
    by_mode = {}
    for r in runs:
        for res in r["results"]:
            tcs = res["tool_calls"]
            tool_s = sum(tc["seconds"] for tc in tcs)
            slowest = max((tc["seconds"] for tc in tcs), default=0)
            g = r["grades"].get(res["mode"])
            rows.append(f"| {r['id']} | {res['mode']} | {fmt_s(res['seconds'])} | {fmt_s(res['model_seconds'])} "
                        f"| {fmt_s(tool_s)} | {res['turns']} | {len(tcs)} | {slowest:.1f}s "
                        f"| {res['output_tokens']:,} | {g['score'] if g else '-'} |")
            by_mode.setdefault(res["mode"], []).append((res, g))
    rows += ["", "| Mode | Questions | Total agent time | Mean | Min | Max | Mean per turn | Mean score | Errors |",
             "|---|---|---|---|---|---|---|---|---|"]
    for mode, items in by_mode.items():
        secs = [res["seconds"] for res, _ in items]
        turns = sum(res["turns"] for res, _ in items)
        model = sum(res["model_seconds"] for res, _ in items)
        scores = [g["score"] for _, g in items if g]
        errors = sum(1 for res, _ in items if res["error"])
        mean_score = f"{sum(scores) / len(scores):.0f}" if scores else "-"
        rows.append(f"| {mode} | {len(items)} | {fmt_s(sum(secs))} | {fmt_s(sum(secs) / len(secs))} "
                    f"| {fmt_s(min(secs))} | {fmt_s(max(secs))} | {model / turns if turns else 0:.0f}s "
                    f"| {mean_score} | {errors} |")
    rows += ["", "| Question | Wall time (both modes + judge) | Judge time |", "|---|---|---|"]
    rows += [f"| {r['id']} | {fmt_s(r['seconds'])} | {fmt_s(r['judge_seconds'])} |" for r in runs]
    rows += ["", f"**Total run time:** {fmt_s(total_seconds)}"]
    return rows


def write_report(runs, outdir: Path, model, total_seconds):
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "results.json").write_text(json.dumps(runs, indent=2, default=str), encoding="utf-8")
    md = [f"# Ontology vs. no-ontology agent comparison\n", f"Model: `{model}` - {datetime.now():%Y-%m-%d %H:%M}\n"]
    md += ["## Run statistics\n"] + stats_tables(runs, total_seconds) + [""]
    if any(r["grades"] for r in runs):
        md.append("| Question | Ontology OFF | Ontology ON |\n|---|---|---|")
        for r in runs:
            g = r["grades"]
            cell = lambda m: f"{g[m]['score']} ({g[m]['verdict']})" if m in g else "-"
            md.append(f"| {r['id']}: {r['title']} | {cell('ontology OFF')} | {cell('ontology ON')} |")
        md.append("")
    for r in runs:
        md.append(f"## {r['id']}: {r['title']}\n\n**Question.** {r['prompt']}\n")
        if r["why_ontology_helps"]:
            md.append(f"**Why the ontology matters.** {r['why_ontology_helps']}\n")
        if r["ground_truth"]:
            md.append(f"**Ground truth.** {r['ground_truth']}\n")
        for res in r["results"]:
            g = r["grades"].get(res["mode"])
            md.append(f"### {res['mode']}" + (f" - score {g['score']}/100" if g else "") + "\n")
            md.append(f"{len(res['tool_calls'])} tool calls, {res['turns']} turns, {res['seconds']} s, "
                      f"{res['input_tokens']:,} input / {res['output_tokens']:,} output tokens\n")
            md.append(res["answer"] or f"_no answer_ ({res['error']})")
            if g and g["missed_or_wrong"]:
                md.append("\n**Judge - missed or wrong:**\n" + "\n".join(f"- {m}" for m in g["missed_or_wrong"]))
            md.append("\n<details><summary>Tool calls</summary>\n")
            for tc in res["tool_calls"]:
                arg = tc["input"].get("query") or tc["input"].get("text") or json.dumps(tc["input"])
                md.append(f"**{tc['name']}**\n```\n{arg}\n```")
            md.append("</details>\n")
    (outdir / "report.md").write_text("\n".join(md), encoding="utf-8")
    return outdir / "report.md"


async def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("questions", nargs="*", help="question ids (see --list)")
    ap.add_argument("--all", action="store_true", help="run every demo question")
    ap.add_argument("--ask", help="run an ad-hoc question (no ground truth / judging)")
    ap.add_argument("--ontology", choices=["on", "off", "both"], default="both",
                    help="attach the ontology MCP server: on, off, or both side by side (default)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--no-judge", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        for q in QUESTIONS:
            print(f"{q.id}  {q.title}\n    {textwrap.fill(q.prompt, 96, subsequent_indent='    ')}\n")
        return

    modes = {"on": [True], "off": [False], "both": [False, True]}[args.ontology]
    proc = ensure_endpoint() if True in modes else None
    kb = KB()
    runs = []
    t0 = time.time()
    outdir = ROOT / "runs" / datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        if args.ask:
            runs.append(await run_question("adhoc", args.ask, modes, args.model, args.effort, False, kb))
        ids = [q.id for q in QUESTIONS] if args.all else args.questions
        if not ids and not args.ask:
            ap.error("give question ids, --all, --ask or --list")
        for qid in ids:
            if qid not in BY_ID:
                ap.error(f"unknown question {qid}; use --list")
            runs.append(await run_question(qid, BY_ID[qid].prompt, modes, args.model, args.effort,
                                           not args.no_judge, kb))
            write_report(runs, outdir, args.model, round(time.time() - t0, 1))  # keep partial results on long runs
    finally:
        if proc:
            proc.terminate()

    if len(runs) > 1 and any(r["grades"] for r in runs):
        print(f"\n{BOLD}SCOREBOARD{RESET}")
        for r in runs:
            g = r["grades"]
            s = "   ".join(f"{m}: {g[m]['score']:>3}" for m in ("ontology OFF", "ontology ON") if m in g)
            print(f"  {r['id']:<4} {r['title']:<50} {s}")
    total = round(time.time() - t0, 1)
    print(f"\n{BOLD}RUN STATISTICS{RESET}\n" + "\n".join(stats_tables(runs, total)))
    report = write_report(runs, outdir, args.model, total)
    print(f"\nreport: {report}")


if __name__ == "__main__":
    asyncio.run(main())
