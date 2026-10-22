import pytest
from repoeval.metrics import pass_at_k, wilson_interval

def test_pass_at_1_equals_rate():
    assert pass_at_k(10, 3, 1) == pytest.approx(0.3)

def test_all_fail_and_all_pass():
    assert pass_at_k(5, 0, 3) == 0.0
    assert pass_at_k(5, 5, 3) == 1.0

def test_k_gt_n_raises():
    with pytest.raises(ValueError):
        pass_at_k(2, 1, 3)

def test_wilson_bounds():
    lo, hi = wilson_interval(5, 10)
    assert 0 <= lo < 0.5 < hi <= 1
