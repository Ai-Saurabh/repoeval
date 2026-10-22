from pathlib import Path
from repoeval.harness import run_all

EX = Path(__file__).resolve().parents[1] / "examples"

def test_harness_classifies_outcomes():
    res = run_all(EX / "tasks/fizzbuzz", EX / "candidates/fizzbuzz", timeout=5)
    a = {r.candidate: r.status for r in res["model-a"]}
    b = {r.candidate: r.status for r in res["model-b"]}
    assert a == {"sample_1.py": "passed", "sample_2.py": "passed", "sample_3.py": "failed"}
    assert b["sample_1.py"] == "passed" and b["sample_2.py"] == "failed"
    assert b["sample_3.py"] == "timeout" and b["sample_4.py"] == "error"
