"""Rubric grading for free-text LLM answers. Deterministic criteria + pluggable judge."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Criterion:
    name: str
    weight: float
    check: Callable[[str], bool]


def contains_all(*terms: str) -> Callable[[str], bool]:
    return lambda text: all(t.lower() in text.lower() for t in terms)


def max_words(n: int) -> Callable[[str], bool]:
    return lambda text: len(text.split()) <= n


def grade(answer: str, rubric: list[Criterion],
          judge: Optional[Callable[[str], float]] = None, judge_weight: float = 0.0) -> dict:
    """Weighted rubric score in [0,1]. `judge` can wrap any LLM API (returns 0..1)."""
    total = sum(c.weight for c in rubric) or 1.0
    hits = {c.name: bool(c.check(answer)) for c in rubric}
    score = sum(c.weight for c in rubric if hits[c.name]) / total
    if judge and judge_weight:
        score = (1 - judge_weight) * score + judge_weight * judge(answer)
    return {"score": round(score, 3), "criteria": hits}
