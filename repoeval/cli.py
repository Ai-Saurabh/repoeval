from __future__ import annotations
import argparse, json
from pathlib import Path
from . import harness, report, validator


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="repoeval", description="Repo validation + LLM code evaluation")
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="validate a repository")
    v.add_argument("repo")
    v.add_argument("--flaky-runs", type=int, default=3)

    e = sub.add_parser("evaluate", help="evaluate candidate solutions against a task")
    e.add_argument("task_dir")
    e.add_argument("candidates_dir")
    e.add_argument("--timeout", type=int, default=20)
    e.add_argument("--out", default=None, help="write markdown report here")
    e.add_argument("--json", default=None, help="write raw JSON here")

    a = ap.parse_args(argv)
    if a.cmd == "validate":
        s = validator.summarize(validator.validate_repo(Path(a.repo), a.flaky_runs))
        print(json.dumps(s, indent=2))
        return 0 if all(c["ok"] for c in s["checks"]) else 1

    task = harness.load_task(Path(a.task_dir))
    res = harness.run_all(Path(a.task_dir), Path(a.candidates_dir), a.timeout)
    md = report.markdown_report(task["id"], res)
    print(md)
    if a.out: Path(a.out).write_text(md)
    if a.json: Path(a.json).write_text(harness.to_json(res))
    return 0
