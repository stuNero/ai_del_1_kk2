import sys
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.constants import REG_FEATURE_COLUMNS

def reg_prepare_features(raw_input: Mapping[str, Any]) -> pd.DataFrame:
    """
    Args:
        `raw_input`: A **mapping** containing the raw input values required to build
            the feature row, keyed by field name. \n
            Required keys: `mental_health`, `stress_level`, `work_hours_per_week`,
            `screen_time_hours`, `meditation_minutes`, `sleep_hours`, `sleep_quality`,
            `physical_activity_hours`, `chronic_stress_no`, `chronic_stress_yes`. \n
            Type `Mapping[str, Any]`.
    Returns:
        A single-row **dataframe** with columns ordered as `REG_FEATURE_COLUMNS`,
        ready to be passed into a fitted model's `predict` method.
    Raises:
        `TypeError`: If `raw_input` is `None` or not a `Mapping`.
        `KeyError`: If `raw_input` is missing one or more of the required keys.
    """
    if not isinstance(raw_input, Mapping):
        raise TypeError("The `raw_input` parameter must be a `Mapping`")

    required_keys = (
        "mental_health",
        "stress_level",
        "work_hours_per_week",
        "screen_time_hours",
        "meditation_minutes",
        "sleep_hours",
        "sleep_quality",
        "physical_activity_hours",
        "chronic_stress_no",
        "chronic_stress_yes",
    )
    missing = [key for key in required_keys if key not in raw_input]
    if missing:
        raise KeyError(f"`raw_input` is missing required keys: {missing}")

    values = [raw_input[key] for key in required_keys]
    return pd.DataFrame([values], columns=REG_FEATURE_COLUMNS)

def reg_predict(model: Any, raw_input: Mapping[str, Any]) -> Any:
    """
    Args:
        `model`: A fitted model exposing a scikit-learn-style `predict` method.
            Type: any object with `.predict(X) -> array-like`.
        `raw_input`: A **mapping** of raw input values, in the same format expected
            by `reg_prepare_features`. \n
            Type `Mapping[str, Any]`.
    Returns:
        The single predicted value for `raw_input`, extracted from `model`'s
        prediction array.
    Raises:
        `TypeError`: If `model` does not implement a callable `.predict` method.
        `TypeError`: If `raw_input` is `None` or not a `Mapping` (propagated from
            `reg_prepare_features`).
        `KeyError`: If `raw_input` is missing a required key (propagated from
            `reg_prepare_features`).
    """
    if not hasattr(model, "predict") or not callable(model.predict):
        raise TypeError("The `model` parameter must implement a callable `predict` method")

    features = reg_prepare_features(raw_input)
    return round(model.predict(features)[0], None)