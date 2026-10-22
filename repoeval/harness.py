"""Sandboxed execution harness: drop a candidate into a repo copy, run tests."""
from __future__ import annotations
import json, re, shutil, subprocess, sys, tempfile, time
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class RunResult:
    candidate: str
    status: str          # passed | failed | timeout | error
    passed: int = 0
    failed: int = 0
    duration_s: float = 0.0
    detail: str = ""


def load_task(task_dir: Path) -> dict:
    task = json.loads((task_dir / "task.json").read_text())
    for key in ("id", "target_file"):
        if key not in task:
            raise ValueError(f"task.json missing '{key}'")
    return task


def _parse_pytest(output: str) -> tuple[int, int, int]:
    passed = sum(int(x) for x in re.findall(r"(\d+) passed", output))
    failed = sum(int(x) for x in re.findall(r"(\d+) failed", output))
    errors = sum(int(x) for x in re.findall(r"(\d+) errors?\b", output))
    return passed, failed, errors


def run_candidate(task_dir: Path, candidate: Path, timeout: int = 20) -> RunResult:
    task = load_task(task_dir)
    with tempfile.TemporaryDirectory(prefix="repoeval_") as tmp:
        work = Path(tmp) / "repo"
        shutil.copytree(task_dir / "repo", work)
        target = work / task["target_file"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(candidate, target)
        start = time.time()
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-x", "--no-header", "-p", "no:cacheprovider"],
                cwd=work, capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return RunResult(candidate.name, "timeout", duration_s=timeout, detail="exceeded time limit")
        out = proc.stdout + proc.stderr
        p, f, e = _parse_pytest(out)
        if proc.returncode == 0:
            status = "passed"
        elif p == 0:
            status = "error"      # collection/import error, nothing ran
        else:
            status = "failed"
        return RunResult(candidate.name, status, p, f, round(time.time() - start, 3),
                         out.strip().splitlines()[-1] if out.strip() else "")


def run_all(task_dir: Path, cand_dir: Path, timeout: int = 20) -> dict[str, list[RunResult]]:
    results: dict[str, list[RunResult]] = {}
    for model in sorted(p for p in cand_dir.iterdir() if p.is_dir()):
        results[model.name] = [run_candidate(task_dir, f, timeout) for f in sorted(model.glob("*.py"))]
    return results


def to_json(results) -> str:
    return json.dumps({m: [asdict(r) for r in rs] for m, rs in results.items()}, indent=2)
