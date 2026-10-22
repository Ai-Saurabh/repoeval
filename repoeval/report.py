from __future__ import annotations
from .metrics import pass_at_k, wilson_interval


def markdown_report(task_id: str, results: dict, ks=(1, 3)) -> str:
    lines = [f"# Evaluation report: `{task_id}`", "",
             "| Model | n | passed | " + " | ".join(f"pass@{k}" for k in ks) + " | 95% CI (pass rate) |",
             "|---|---|---|" + "---|" * len(ks) + "---|"]
    for model, rs in results.items():
        n, c = len(rs), sum(r.status == "passed" for r in rs)
        cells = [f"{pass_at_k(n, c, k):.2f}" if k <= n else "n/a" for k in ks]
        lo, hi = wilson_interval(c, n)
        lines.append(f"| {model} | {n} | {c} | " + " | ".join(cells) + f" | {lo:.2f}-{hi:.2f} |")
    lines += ["", "## Failure breakdown", "", "| Model | Sample | Status | Detail |", "|---|---|---|---|"]
    for model, rs in results.items():
        for r in rs:
            if r.status != "passed":
                lines.append(f"| {model} | {r.candidate} | {r.status} | {r.detail} |")
    return "\n".join(lines) + "\n"
