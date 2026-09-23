---
description:
  title: "Week 3 Lab: MLflow Integration"
  summary: |
    Use the Week 2 stack properly: structured logging with plots as artifacts,
    a parameter sweep producing comparable runs, server-side run search, and the
    model registry — registering a version, promoting it with an alias, and
    walking the traceability chain back to the params that produced it.
---

# Week 3 Lab: MLflow Integration

Week 2 built the infrastructure and proved it worked by logging **one** run. One run
is not an experiment: you cannot rank it, you cannot see a trend, and you cannot say
which model is *the* model.

This week you use MLflow as an engineering discipline:

- **structured logging** — batched params and metrics, tags you can search on, a
  model signature, and diagnostic plots stored as artifacts
- **a parameter sweep** — one parent run with one child run per configuration
- **run search** — finding the winner with a query
- **the model registry** — a named model, immutable versions, and a movable alias
- **traceability** — walking backwards from a deployed alias to the exact params,
  metrics, and git commit that produced it

The infrastructure does not change at all. `compose.yaml` is the Week 2 stack — **every exercise this week is in Python.**

## Based on

This lab follows official tutorials with minimal changes — keep them open as references:

- **MLflow tracking quickstart (primary template):** https://mlflow.org/docs/latest/ml/getting-started/quickstart/
- **Hyperparameter tuning — nested runs and comparing runs:** https://mlflow.org/docs/latest/ml/getting-started/hyperparameter-tuning/
- **Model Registry concepts:** https://mlflow.org/docs/latest/ml/model-registry/
- **Model Registry workflows:** https://mlflow.org/docs/latest/ml/model-registry/workflow/
- **MLflow tracking concepts and run search:** https://mlflow.org/docs/latest/ml/tracking/

**Required deviations from the official tutorials**:

1. **Aliases instead of stages.** MLflow deprecated model *stages* (`None`/`Staging`/`Production`/`Archived` and
   `transition_model_version_stage`) in version 2.9, and the official registry tutorial
   now uses **aliases** exclusively. This lab therefore promotes with
   `set_registered_model_alias` and the URI `models:/diabetes-classifier@staging`.
   You will meet the old API in older blog posts and tutorial videos — recognise it as
   historical.
2. **No Optuna.** The official sweep tutorial drives the grid with Optuna; we use a plain
   `for` loop over a small grid to minimise dependencies and keep the focus on MLflow.
3. **A remote tracking server, not a local `mlruns/` directory.** We point at the
   containerized Week 2 stack via `MLFLOW_TRACKING_URI=http://127.0.0.1:5500`.
4. **`name=` instead of `artifact_path=`** in `log_model`. MLflow 3 deprecates
   `artifact_path`.
5. **The Pima diabetes dataset** instead of the tutorial's toy dataset, per the course's
   one-running-example rule.

## Prerequisites

- Docker Desktop (macOS/Windows) or Docker Engine + Compose plugin (Linux) — version 24+
- At least 16 GB RAM
- `uv` — https://docs.astral.sh/uv/getting-started/installation/
- Ports **5500, 5510, 5511, 5532** free on your host (the 55xx block; see `.env.example`)
- **Stop your Week 2 stack first.** It uses the same host ports:
  ```bash
  cd ../../week-02-local-services/starter && docker compose down
  ```

---

## Step 1 — Install Python dependencies

From this directory (`labs/week-03-mlflow-integration/starter/`):

```bash
uv sync --all-groups
```

New this week: **matplotlib**, for the diagnostic plots in Exercise 2.

## Step 2 — Create your local configuration

```bash
cp .env.example .env
```

Read the new `MLFLOW_REGISTERED_MODEL_NAME` / `MLFLOW_MODEL_ALIAS` / `MLFLOW_MODEL_OWNER`
block at the bottom, and set `MLFLOW_MODEL_OWNER` to your own name — it gets recorded as a
governance tag when you promote a model. **Never commit `.env`** — it is git-ignored.

Notice what is *absent* from the client config: any `AWS_*` credentials. Your pipeline
talks only to the tracking server, which holds the MinIO keys and proxies artifacts on your
behalf.

## Step 3 — Run the tests (no stack required)

```bash
uv run pytest tests/ -v
```

Expected: **16 passed, 10 skipped**. Each skipped test names the exercise that unlocks it —
implement the code, delete that test's `@pytest.mark.skip` line, and the test becomes your
check that you got it right.

## Step 4 — Bring up the stack

```bash
docker compose up -d --wait
```

This is the Week 2 stack, unchanged. All four services must report healthy.

| Service | URL | Credentials |
| --- | --- | --- |
| MLflow UI | http://localhost:5500 | none |
| MinIO console | http://localhost:5511 | `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` from `.env` |
| Postgres | `localhost:5532` | `POSTGRES_USER` / `POSTGRES_PASSWORD` from `.env` |

The MLflow experiment list should be **empty**. This lab is a separate Compose project with
its own database volume, so none of your Week 2 runs appear here.

---

## Exercises

Complete these in order — each builds on the previous. Every exercise has a `make` target,
and every `TODO(student)` is in `src/week_03_mlflow_integration/`.

Two exercises ask for a **written answer**. Put those in a file called `answers.md` in this
directory (it is git-ignored, so it stays yours).

### Exercise 1 — Log one run properly

Open `src/week_03_mlflow_integration/tracking.py` and fill in the four blanks in
`log_training_run`: `log_params`, `set_tags`, `log_metrics`, and `log_model`.

Week 2 logged three params with three separate `log_param` calls. Here you log them in one
batched call, because one call is one HTTP round-trip and three calls are three. You also add
two new things:

- **tags** — free-form labels. Params exist so someone can *reproduce* a run; tags exist so
  someone can *find* it. The `git_commit` tag is the most important one you will ever
  log: it is the link from a recorded metric back to the exact code.
- **a signature and input example** — these make the logged model self-describing.

```bash
make run
```

Then open the run in the UI. Confirm you see a populated params table, five metrics, your
tags, and — on the logged model — a filled-in **Schema** tab.

### Exercise 2 — Log two plots as artifacts

Implement `roc_curve_figure` and `confusion_matrix_figure` in
`src/week_03_mlflow_integration/plots.py`, then log them from `log_training_run` with
`mlflow.log_figure`.

Both functions **return** a `Figure` and never call `plt.show()` or `plt.savefig()`.

```bash
make run
```

In the UI, the run's Artifacts tab should show `plots/roc_curve.png` and
`plots/confusion_matrix.png`, rendered inline. Read the confusion matrix: how many false positives and false negatives did your model make on the test set?

### Exercise 3 — Sweep six configurations

Implement the loop in `run_sweep` (`tracking.py`). `SWEEP_GRID` is already defined: four
regularisation strengths for logistic regression and two forest sizes.

```bash
make sweep
```

In the UI: expand the `sweep` run to see its six children, select all six, and click
**Compare**. Then switch to the **Parallel Coordinates** view.

### Exercise 4 — Find the winner without scrolling

Implement `search_sweep_runs` in `tracking.py` using `mlflow.search_runs` with a
`filter_string` and an `order_by`.

```bash
make best
```

The filter string is evaluated **by the tracking server, against Postgres**.
Prove it to yourself: call the function with `min_f1=0.99` and confirm you get zero rows rather than six.

**Written answer** (in `answers.md`):

1. Rank the six runs by `f1`, then by `roc_auc`. Do you get the same winner? If not, why
   might two reasonable metrics disagree about the same six models?
2. Look at the confusion matrix of your F1 winner. Would you ship it? Give one concrete
   reason the highest test F1 is a *candidate* rather than a decision.
3. Name one thing MLflow recorded about these runs that you did not have to remember.

### Exercise 5 — Register the winning model

Implement `register_best_model` in `src/week_03_mlflow_integration/registry.py`.

Note the URI form in the docstring, and use it: `f"runs:/{run_id}/model"`. It matters more
than it looks — see the troubleshooting table below.

```bash
make register
```

Version **1** now exists. In the UI's **Models** tab, open it and follow the **Source run**
link back to the sweep child it came from.

Now run it once more:

```bash
make register   # the same model, registered a second time
```

You get version **2**, from the same run. Versions are immutable and monotonic: you never
edit version 1, you register version 2.

> **Which version gets promoted.** `make promote` always acts on the *newest* version. The
> reference output in the solution was captured after a **single** registration, so it
> promotes and traces version 1. If you registered twice, your `make trace` shows version 2.

### Exercise 6 — Promote with an alias, then walk the chain back *(written answer)*

Implement `promote_to_staging` and `trace_alias` in `registry.py`.

```bash
make promote
make trace
```

`promote_to_staging` does two separable things, and only the second is an API call:

1. It records the **evidence** — the validation metrics, who promoted it, and when — as
   version tags. Notice it reads those metrics back from the source run, so the tag cannot drift from what was actually measured.
2. It **moves a pointer**. The version does not change. `@staging` simply resolves somewhere new.

You assign two aliases, `staging` and `champion`, to the same version.

`make trace` then walks backwards: alias → version → `run_id` → params, metrics, and the
`git_commit` tag. The last line loads the model through `models:/<name>@staging` and predicts
five rows, which proves the alias resolves through the tracking server's artifact proxy with
no object-store credentials on your side.

**Written answer** (in `answers.md`):

1. Write out the traceability chain as an ordered list of lookups: starting from
   `models:/diabetes-classifier@staging`, what call do you make at each hop to end up at the
   training code? Which hop is *not* MLflow's job?
2. What can an alias do that a fixed `Staging` stage could not? Give at least two things.
3. Walk the chain as far back as it goes. It ends at a **file path** — `data/diabetes.csv`.
   What does that mean for the metrics you just recorded, and what would you need in order to
   close that last gap?

### Exercise 7 — Commit your work

```bash
git status          # .env, .venv/, and answers.md must NOT appear
git add labs/week-03-mlflow-integration/starter
git commit -m "week03: log structured runs, sweep, register and promote a model"
```

---

## Where the artifacts actually live

Open the MinIO console (http://localhost:5511) and browse the `mlflow-artifacts` bucket.
Run artifacts and model artifacts sit in **different prefixes**:

```
mlflow-artifacts/
  <experiment_id>/
    <run_id>/artifacts/plots/roc_curve.png            <- mlflow.log_figure
    <run_id>/artifacts/plots/confusion_matrix.png        (a RUN artifact)
    models/m-<32 hex chars>/artifacts/MLmodel          <- mlflow.sklearn.log_model
    models/m-<32 hex chars>/artifacts/model.pkl           (a first-class logged model,
    models/m-<32 hex chars>/artifacts/requirements.txt     addressable independently of
    models/m-<32 hex chars>/artifacts/python_env.yaml      the run that produced it)
    models/m-<32 hex chars>/artifacts/input_example.json
```

In MLflow 3 a logged model is its own entity, not a folder inside a run.
It is exactly why registering from `runs:/<run_id>/model` prints the warning in the troubleshooting table below.

## Tear-down

```bash
docker compose down      # stop; your runs persist in the named volumes
docker compose down -v   # stop AND wipe the volumes for a from-scratch re-run
```

## Repository structure

```
starter/
├── compose.yaml                    # the Week 2 stack, complete — no TODOs here
├── mlflow.Dockerfile               # pinned MLflow server image
├── Makefile                        # one target per exercise
├── bootstrap.sh                    # one-time uv lock (already committed)
├── .env.example                    # copy to .env
├── pyproject.toml / uv.lock        # + matplotlib, new this week
├── data/diabetes.csv
├── src/
│   ├── main.py
│   └── week_03_mlflow_integration/
│       ├── config.py               # + registry settings (complete)
│       ├── data.py                 # unchanged from Weeks 1-2
│       ├── model.py                # + build_model, + roc_auc (complete)
│       ├── plots.py                # TODO: Exercise 2
│       ├── tracking.py             # TODO: Exercises 1, 3, 4
│       ├── registry.py             # TODO: Exercises 5, 6
│       └── cli.py                  # the subcommand dispatcher (complete)
└── tests/
    ├── conftest.py                 # the "is the stack up?" guard, as fixtures
    ├── test_config.py              # 7 tests, no stack needed
    ├── test_smoke.py               # 7 tests, no stack needed
    ├── test_plots.py               # 4 tests, no stack needed
    ├── test_tracking.py            # 4 tests, needs the stack
    └── test_registry.py            # 4 tests, needs the stack
```

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `Bind for 0.0.0.0:5500 failed: port is already allocated` | Your Week 2 stack (or another Week 3 stack) is still running. `cd ../../week-02-local-services/starter && docker compose down`. Only one stack can hold the 55xx ports at a time. |
| `WARNING ... Run with id ... has no artifacts at artifact path 'model', registering model based on models:/m-... instead` | **Expected, not an error.** MLflow 3 stores logged-model files outside the run's artifact root (see the layout above). Your version is still created and its Source-run link still works. |
| `ModelVersion.run_id` is empty, and `make trace` cannot find the run | You registered from `model_info.model_uri` instead of `f"runs:/{run_id}/model"`. Only the `runs:/` form records `run_id` against the open-source registry. `tests/test_registry.py` checks exactly this. |
| `make best` returns no rows even though the sweep ran | Check the `filter_string` quoting: tag and param values need single quotes *inside* the Python string (`tags.sweep = 'week3-baseline'`), the operator is `=` not `==`, and metric comparisons are bare numbers (`metrics.f1 > 0.5`). |
| `MlflowException: Could not find experiment with name ...` | Run `make sweep` before `make best` — the experiment is created on first write. |
| `UserWarning: Hint: Inferred schema contains integer column(s)` | Expected. `infer_signature` notices that integer columns cannot carry missing values. Our dataset hides its missing values as zeros — deliberately, until Week 5. Leave it alone. |
| Nothing appears in the MLflow UI | Confirm the stack is healthy (`docker compose ps`) and that `MLFLOW_TRACKING_URI` in `.env` is `http://127.0.0.1:5500`. |
| `RuntimeWarning: More than 20 figures have been opened` | You are missing `plt.close(figure)` after each `mlflow.log_figure` — the sweep opens 12 figures. |
| Want to start completely over | `docker compose down -v && docker compose up -d --wait`. This wipes both the Postgres metadata and the MinIO artifacts. |

## Next steps

Walk your traceability chain all the way back and it stops at `data/diabetes.csv` — a
**path**. Nothing you recorded this week says which bytes were in that file.
Edit one row and every metric above becomes obsolete. Week 4 closes that gap with DVC:
dataset snapshots tracked by content hash, MinIO as the storage remote, and a data version
linked to each MLflow run.
