"""Evaluation metrics for code-generation benchmarks."""
from math import comb, sqrt


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased pass@k estimator (Chen et al., 2021).

    n: samples generated, c: samples that passed, k: budget.
    """
    if n < k:
        raise ValueError("k cannot exceed number of samples n")
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


def wilson_interval(passed: int, total: int, z: float = 1.96):
    """Wilson score interval for a pass rate."""
    if total == 0:
        return (0.0, 0.0)
    p = passed / total
    d = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / d
    half = z * sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))
