"""Static + dynamic repository validation."""
from __future__ import annotations
import subprocess, sys
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""


def _exists_any(root: Path, names) -> bool:
    return any((root / n).exists() for n in names)


def validate_repo(root: Path, flaky_runs: int = 3, timeout: int = 60, run_tests: bool = True) -> list[Check]:
    root = Path(root)
    checks = [
        Check("readme", _exists_any(root, ["README.md", "README.rst"]), "README present"),
        Check("license", _exists_any(root, ["LICENSE", "LICENSE.md"]), "LICENSE present"),
        Check("dependency_manifest", _exists_any(root, ["pyproject.toml", "requirements.txt", "setup.py"]),
              "dependency manifest present"),
        Check("tests_dir", any(root.glob("tests/test_*.py")) or any(root.glob("test_*.py")), "pytest files found"),
        Check("ci_config", (root / ".github/workflows").exists(), "CI workflow present"),
    ]
    if not run_tests:
        return checks
    # Dynamic: run suite repeatedly to detect failures / flakiness.
    outcomes = []
    for _ in range(flaky_runs):
        try:
            p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                               cwd=root, capture_output=True, text=True, timeout=timeout)
            outcomes.append(p.returncode == 0)
        except subprocess.TimeoutExpired:
            outcomes.append(False)
    checks.append(Check("tests_pass", all(outcomes), f"{sum(outcomes)}/{flaky_runs} runs green"))
    checks.append(Check("deterministic", len(set(outcomes)) == 1,
                        "stable across runs" if len(set(outcomes)) == 1 else "FLAKY: mixed results"))
    return checks


def summarize(checks: list[Check]) -> dict:
    return {"score": f"{sum(c.ok for c in checks)}/{len(checks)}",
            "checks": [asdict(c) for c in checks]}
