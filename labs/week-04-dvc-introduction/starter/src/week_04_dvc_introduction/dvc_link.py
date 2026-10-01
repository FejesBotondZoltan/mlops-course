"""Record the DVC data version on the MLflow run (Exercises 6 and 7)."""

from __future__ import annotations

import mlflow
import mlflow.data
from mlflow.data.pandas_dataset import PandasDataset

from .config import Settings
from .data import TARGET_COLUMN
from .datasets import file_md5
from .dvc_meta import pointer_md5, remote_object_uri


def dvc_data_url(settings: Settings) -> str:
    """The s3:// URI of the current data version in the DVC remote.

    Uses `dvc.api.get_url`, or builds the same URI from the pointer's md5 when
    the file is outside a DVC project.
    """
    try:
        import dvc.api

        return str(dvc.api.get_url(str(settings.measurements_path)))
    except Exception:
        return remote_object_uri(settings, pointer_md5(settings.measurements_path))


def log_data_version(settings: Settings) -> dict:
    """Tag the active run with the data version. Returns what was logged.

    TODO(student) — Exercise 6, part 1: set four tags on the active run and
    return them as a dict. The tests check these keys: dvc_md5 (from the pointer,
    see dvc_meta.py), dvc_url (the helper above), dvc_remote ("<bucket>/<remote
    path>" from settings) and data_file (the file name).
    """
    md5 = pointer_md5(settings.measurements_path)
    url = dvc_data_url(settings)
    remote = f"{settings.dvc_bucket}/{settings.dvc_remote_path}"
    data_file = settings.measurements_path.name

    tags = {
        "dvc_md5": md5,
        "dvc_url": url,
        "dvc_remote": remote,
        "data_file": data_file,
    }

    mlflow.set_tags(tags)
    return tags


def log_dataset_input(frame, settings: Settings, source: str) -> str | None:
    """Log the training data as an MLflow Dataset input. Returns its digest.

    TODO(student) — Exercise 6, part 2: build an MLflow dataset from `frame`
    (name "diabetes-measurements", the target column from .data, and `source`),
    log it as an input with context "training", and return its digest.
    Reference: https://mlflow.org/docs/latest/ml/dataset/
    """
    dataset: PandasDataset = mlflow.data.from_pandas(
        frame,
        source=source,
        name="diabetes-measurements",
        targets=TARGET_COLUMN,
    )
    mlflow.log_input(dataset, context="training")
    return dataset.digest


def require_data_added(settings: Settings) -> str:
    """Check that the data on disk is the data the pointer names. Returns its md5.

    TODO(student) — Exercise 7 (optional): compare the md5 of the file on disk
    (file_md5) with the md5 in its pointer (pointer_md5). If they differ, raise a
    RuntimeError whose message tells the user to run `dvc add`.
    """
    _ = file_md5  # keep the import meaningful until you implement the body
    return ""  # placeholder: no check yet
