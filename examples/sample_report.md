# Evaluation report: `fizzbuzz`

| Model | n | passed | pass@1 | pass@3 | 95% CI (pass rate) |
|---|---|---|---|---|---|
| model-a | 3 | 2 | 0.67 | 1.00 | 0.21-0.94 |
| model-b | 4 | 1 | 0.25 | 0.75 | 0.05-0.70 |

## Failure breakdown

| Model | Sample | Status | Detail |
|---|---|---|---|
| model-a | sample_3.py | failed | 1 failed, 1 passed in 0.02s |
| model-b | sample_2.py | failed | 1 failed, 1 passed in 0.02s |
| model-b | sample_3.py | timeout | exceeded time limit |
| model-b | sample_4.py | error | 1 error in 0.11s |
