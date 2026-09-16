# Week 1 Lab — Reference Solution

Completed reference solution for all exercises. Instructors can use it to verify student submissions.

## Changes from starter

| File | Exercise | What changed |
| --- | --- | --- |
| `src/week_01_env_setup/model.py` | 2 | Added `train_random_forest` |
| `src/week_01_env_setup/cli.py` | 2 | Trains and evaluates both LR and RF |
| `tests/test_data.py` | 3 | Implemented `test_split_ratios`, removed skip marker |

## Running the solution

```bash
cd solution
uv sync --all-groups
uv run python src/main.py
uv run pytest tests/ -v   # expected: 4 passed
```

Expected metrics (seed 42): Logistic Regression F1 = 0.5785, Random Forest F1 = 0.6066.

> Model answers and the grading rubric are kept instructor-only in `.agents/grading/week-01.md` (not shipped with student or solution releases).
