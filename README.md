# repoeval

[![CI](https://github.com/saurabhub/repoeval/actions/workflows/ci.yml/badge.svg)](https://github.com/saurabhub/repoeval/actions)

A small, dependency-free toolkit for **LLM code evaluation** and **repository validation**:

- **Sandboxed harness**: drops each model-generated solution into a fresh copy of a repo, runs the test suite with a hard timeout, and classifies the outcome as `passed`, `failed`, `timeout` or `error` (syntax/import failure).
- **Metrics**: unbiased **pass@k** estimator (Chen et al., 2021) and Wilson confidence intervals, so small samples are not over-interpreted.
- **Repo validator**: checks README, LICENSE, dependency manifest, tests, CI, and runs the suite repeatedly to catch **flaky** tests.
- **Rubric grader**: weighted, deterministic criteria for free-text answers, with a pluggable LLM-judge hook.

## Quick start

```bash
pip install -e ".[dev]"
pytest -q
python -m repoeval evaluate examples/tasks/fizzbuzz examples/candidates/fizzbuzz --out report.md
python -m repoeval validate .
```

## Sample output

| Model | n | passed | pass@1 | pass@3 | 95% CI (pass rate) |
|---|---|---|---|---|---|
| model-a | 3 | 2 | 0.67 | 1.00 | 0.21-0.94 |
| model-b | 4 | 1 | 0.25 | 0.75 | 0.05-0.70 |

Failure modes are broken down per sample (wrong logic, infinite loop caught by timeout, syntax error). See `examples/sample_report.md`.

## Task format

```
tasks/<id>/task.json        # {"id": "...", "prompt": "...", "target_file": "solution.py"}
tasks/<id>/repo/            # starter repo containing the tests
candidates/<id>/<model>/*.py  # one file per sampled generation
```

## Design notes

- Each run uses an isolated temp copy, so candidates cannot contaminate each other or the source repo.
- Timeouts and import errors are treated as distinct from logic failures, which matters when diagnosing model behaviour.
- `pass@k` uses the combinatorial estimator, not the naive "any of k" rate.
- Limitation: subprocess isolation is not a security sandbox. For untrusted code, run inside Docker or gVisor.

## Roadmap

- Docker-based sandbox backend
- Multi-language tasks (JS, Go)
- LLM-as-judge adapters with agreement metrics (Cohen's kappa)
