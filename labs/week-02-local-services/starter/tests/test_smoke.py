"""Smoke tests for the Week 2 pipeline.

These tests do NOT require a running Docker stack.
They verify the pipeline logic in isolation: data loading, model training,
and metric shapes — the same guarantees Week 1 tests gave, plus the new
MLflow settings. Any test that would require a live MLflow server is
decorated with @pytest.mark.skip so the starter passes out of the box.
"""
import pytest

from week_02_local_services.config import load_settings
from week_02_local_services.data import build_dataset, load_dataframe
from week_02_local_services.model import evaluate_model, train_logistic_regression


def test_dataframe_loads() -> None:
    """The diabetes CSV loads and has the expected shape."""
    settings = load_settings()
    frame = load_dataframe(settings)
    assert len(frame) == 768
    assert "outcome" in frame.columns


def test_dataset_split_sizes() -> None:
    """Train + test row counts sum to total rows."""
    settings = load_settings()
    frame = load_dataframe(settings)
    x_train, x_test, y_train, y_test = build_dataset(settings)
    assert len(x_train) + len(x_test) == len(frame)


def test_logistic_regression_returns_model() -> None:
    """train_logistic_regression returns a fitted scikit-learn Pipeline."""
    from sklearn.pipeline import Pipeline

    settings = load_settings()
    x_train, x_test, y_train, y_test = build_dataset(settings)
    model = train_logistic_regression(x_train, y_train, settings)
    assert isinstance(model, Pipeline)


def test_evaluate_model_keys() -> None:
    """evaluate_model returns a dict with the expected metric keys."""
    settings = load_settings()
    x_train, x_test, y_train, y_test = build_dataset(settings)
    model = train_logistic_regression(x_train, y_train, settings)
    metrics = evaluate_model(model, x_test, y_test)
    assert set(metrics.keys()) == {"accuracy", "precision", "recall", "f1"}


def test_seed_42_metrics() -> None:
    """Seed 42 reproduces the Week 1 baseline metrics (LR F1 ≈ 0.5785)."""
    settings = load_settings()
    x_train, x_test, y_train, y_test = build_dataset(settings)
    model = train_logistic_regression(x_train, y_train, settings)
    metrics = evaluate_model(model, x_test, y_test)
    # These must match Week 1 solution exactly — if they change, the dataset
    # or pipeline was modified unintentionally.
    assert metrics["f1"] == pytest.approx(0.5785, abs=0.001)
    assert metrics["accuracy"] == pytest.approx(0.7344, abs=0.001)


@pytest.mark.skip(
    reason="Exercise 3 — implement MLflow logging in cli.py, then remove this skip."
)
def test_mlflow_run_logged() -> None:
    """After Exercise 3: confirm that main() logs a run to the tracking server.

    TODO(student) — Exercise 3, step 4:
    1. Ensure the stack is running: docker compose up -d --wait
    2. Delete the @pytest.mark.skip line above.
    3. Implement this test:
       - Call main() (from week_02_local_services.cli import main)
       - Use the MLflow client to query the last run in the experiment:
           import mlflow
           client = mlflow.tracking.MlflowClient(settings.mlflow_tracking_uri)
           runs = client.search_runs(experiment_ids=[...])
           assert len(runs) > 0
       - Assert the run has params and at least one metric.
    Note: this test requires a running MLflow server. Guard it with a
    reachability check or document that it needs the stack.
    """
    raise NotImplementedError
