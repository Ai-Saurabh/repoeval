from pathlib import Path
from repoeval.rubric import Criterion, contains_all, max_words, grade
from repoeval.validator import validate_repo

def test_rubric_scoring():
    rub = [Criterion("mentions_cache", 2, contains_all("cache")), Criterion("short", 1, max_words(5))]
    assert grade("use a cache", rub)["score"] == 1.0
    assert grade("this is a very long answer without it", rub)["score"] == 0.0

def test_validator_on_self():
    root = Path(__file__).resolve().parents[1]
    names = {c.name: c.ok for c in validate_repo(root, run_tests=False)}
    assert names["readme"] and names["tests_dir"] and names["ci_config"]
