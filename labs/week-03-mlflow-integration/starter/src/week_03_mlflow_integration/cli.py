"""Command-line entry point — one subcommand per lab exercise.

    uv run python src/main.py run        # Exercises 1-2: one fully-logged run
    uv run python src/main.py sweep      # Exercise 3: parent + six children
    uv run python src/main.py best       # Exercise 4: server-side run search
    uv run python src/main.py register   # Exercise 5: register the winner
    uv run python src/main.py promote    # Exercise 6: move the alias
    uv run python src/main.py trace      # Exercise 6: walk the chain back
    uv run python src/main.py all        # everything, in order (the default)

All printing lives here. The modules stay quiet so they remain testable.
"""

from __future__ import annotations

import argparse
import json

from .config import Settings, load_settings
from .data import build_dataset, load_dataframe
from .registry import (
    latest_version,
    load_aliased_model,
    promote_to_staging,
    register_best_model,
    trace_alias,
)
from .tracking import (
    SWEEP_GRID,
    connect,
    find_best_run,
    format_comparison_table,
    log_training_run,
    run_sweep,
    search_sweep_runs,
)


def _banner(settings: Settings) -> None:
    frame = load_dataframe(settings)
    print("Week 3 — MLflow experiment tracking and model registry")
    print("=" * 54)
    print(f"Dataset:          {settings.data_path.name} ({len(frame)} patients)")
    print(f"Diabetes rate:    {frame['outcome'].mean():.1%}")
    print(f"Random seed:      {settings.random_seed}")
    print(f"Tracking server:  {settings.mlflow_tracking_uri}")
    print(f"Experiment:       {settings.mlflow_experiment_name}")
    print(f"Registered model: {settings.registered_model_name}")
    print()


def cmd_run(settings: Settings) -> None:
    """Exercises 1-2 — one deliberate, fully-instrumented run."""
    print("── Exercise 1-2: one fully-logged run ──")
    connect(settings)
    result = log_training_run(settings, "logreg", {"C": 1.0})
    print(f"Run name:  {result.run_name}")
    print(f"Run ID:    {result.run_id}")
    print("Metrics:")
    print(json.dumps(result.metrics, indent=2))
    print()
    print(f"Open the run: {settings.mlflow_tracking_uri}")
    print("  -> the Artifacts tab has plots/roc_curve.png and")
    print("     plots/confusion_matrix.png; the model has a populated Schema tab.")
    print()


def cmd_sweep(settings: Settings) -> None:
    """Exercise 3 — the parameter sweep."""
    print(f"── Exercise 3: sweeping {len(SWEEP_GRID)} configurations ──")
    results = run_sweep(settings)
    for result in results:
        print(
            f"  {result.run_name:<26} "
            f"f1={result.metrics['f1']:.4f}  "
            f"roc_auc={result.metrics['roc_auc']:.4f}"
        )
    print()
    if not results:
        print("No child runs — implement the loop in run_sweep() (Exercise 3).")
        print()
        return
    print(f"{len(results)} child runs logged under one parent run.")
    print("In the UI: select all the children -> Compare -> Parallel Coordinates.")
    print()


def cmd_best(settings: Settings) -> None:
    """Exercise 4 — find the winner with a server-side query."""
    print("── Exercise 4: server-side run search ──")
    frame = search_sweep_runs(settings)
    print(format_comparison_table(frame))
    print()
    if frame.empty:
        print("No rows — implement search_sweep_runs() in tracking.py (Exercise 4),")
        print("and make sure you have run 'make sweep' first (Exercise 3).")
        print()
        return
    run_id = find_best_run(settings)
    print(f"Best run by F1: {run_id}")
    print()


def cmd_register(settings: Settings) -> None:
    """Exercise 5 — register the winning run's model."""
    print("── Exercise 5: register the best run's model ──")
    try:
        run_id = find_best_run(settings)
    except RuntimeError as error:
        print(error)
        print()
        return
    version = register_best_model(settings, run_id)
    if version is None:
        print("Not implemented yet — see the TODO in registry.py (Exercise 5).")
        print()
        return
    print(f"Registered:  {version.name}")
    print(f"Version:     {version.version}")
    print(f"Source run:  {version.run_id or '(empty — see registry.py docstring)'}")
    print()


def cmd_promote(settings: Settings) -> None:
    """Exercise 6 — promote the newest version."""
    print("── Exercise 6: promote to @{alias} ──".format(alias=settings.model_alias))
    try:
        version = latest_version(settings)
    except RuntimeError as error:
        print(error)
        print()
        return
    promoted = promote_to_staging(settings, version.version)
    if promoted is None:
        print("Not implemented yet — see the TODO in registry.py (Exercise 6).")
        print()
        return
    print(f"Version {promoted.version} now carries aliases: {list(promoted.aliases)}")
    print("Governance tags:")
    print(json.dumps(promoted.tags, indent=2))
    print()


def cmd_trace(settings: Settings) -> None:
    """Exercise 6 — walk the traceability chain backwards."""
    print("── Exercise 6: traceability walk-back ──")
    chain = trace_alias(settings)
    if not chain:
        print("Not implemented yet — see the TODO in registry.py (Exercise 6).")
        print()
        return
    print(f"1. Model URI:   {chain['model_uri']}")
    print(f"2. Version:     {chain['version']}  (aliases: {chain['aliases']})")
    print(f"3. Run ID:      {chain['run_id']}  ({chain['run_name']})")
    print(f"4. Git commit:  {chain['git_commit']}")
    print("5. Params that produced it:")
    print(json.dumps(chain["params"], indent=6))
    print("   Version tags (the promotion evidence):")
    print(json.dumps(chain["version_tags"], indent=6))
    print()

    # The alias resolves through the artifact proxy — no MinIO credentials here.
    model = load_aliased_model(settings)
    _, x_test, _, _ = build_dataset(settings)
    predictions = model.predict(x_test.head(5))
    print(f"Loaded via the alias and predicted 5 rows: {list(predictions)}")
    print()


def cmd_all(settings: Settings) -> None:
    """Exercises 1-6, in order."""
    cmd_run(settings)
    cmd_sweep(settings)
    cmd_best(settings)
    cmd_register(settings)
    cmd_promote(settings)
    cmd_trace(settings)


COMMANDS = {
    "run": cmd_run,
    "sweep": cmd_sweep,
    "best": cmd_best,
    "register": cmd_register,
    "promote": cmd_promote,
    "trace": cmd_trace,
    "all": cmd_all,
}


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="week-03-mlflow-integration",
        description="Week 3 lab — MLflow experiment tracking and model registry.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="all",
        choices=sorted(COMMANDS),
        help="which exercise to run (default: all)",
    )
    args = parser.parse_args()

    settings = load_settings()
    _banner(settings)
    COMMANDS[args.command](settings)
