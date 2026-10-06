"""Grade a finished run outside the demo (e.g. by Claude Code in chat) and rebuild its report.

  python demo/grade_run.py export runs/<dir>   # writes runs/<dir>/grading_packet.md for the grader
  python demo/grade_run.py apply runs/<dir>    # merges runs/<dir>/grades.json, rewrites report.md

grades.json maps question id -> mode -> grade, using the judge's schema:
  {"q0": {"ontology OFF": {"score": 50, "verdict": "partially_correct", "correct_points": [...],
                           "missed_or_wrong": [...], "summary": "..."}, "ontology ON": {...}}, ...}
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from judge import PROMPT, SCHEMA  # noqa: E402
from questions import BY_ID, KB  # noqa: E402
from run_demo import write_report  # noqa: E402


def export(rundir: Path):
    runs = json.loads((rundir / "results.json").read_text(encoding="utf-8"))
    kb = KB()
    out = ["# Grading packet\n",
           "Grade each answer with the rules below and write `grades.json` next to this file "
           "(question id -> mode -> grade). Grade schema:\n",
           "```json\n" + json.dumps(SCHEMA, indent=2) + "\n```\n"]
    for r in runs:
        q = BY_ID.get(r["id"])
        if not q:
            continue
        truth, facts = q.ground_truth(kb)
        for res in r["results"]:
            out.append(f"---\n\n## {r['id']} / {res['mode']}\n")
            out.append(PROMPT.format(question=r["prompt"], truth=truth, facts=json.dumps(facts, default=str),
                                     answer=res["answer"] or f"(no answer: {res['error']})"))
            out.append("")
    path = rundir / "grading_packet.md"
    path.write_text("\n".join(out), encoding="utf-8")
    print(path)


def apply(rundir: Path):
    runs = json.loads((rundir / "results.json").read_text(encoding="utf-8"))
    grades = json.loads((rundir / "grades.json").read_text(encoding="utf-8"))
    for r in runs:
        if r["id"] in grades:
            r["grades"] = grades[r["id"]]
    report = rundir / "report.md"
    m = re.search(r"Model: `([^`]+)`", report.read_text(encoding="utf-8")) if report.exists() else None
    total = sum(r["seconds"] for r in runs)  # question wall times; excludes endpoint start-up
    print(write_report(runs, rundir, m.group(1) if m else "unknown", total))
    for r in runs:
        print(f"  {r['id']:<4} " + "   ".join(f"{mode}: {g['score']:>3}" for mode, g in r["grades"].items()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["export", "apply"])
    ap.add_argument("rundir", type=Path)
    a = ap.parse_args()
    {"export": export, "apply": apply}[a.action](a.rundir)
