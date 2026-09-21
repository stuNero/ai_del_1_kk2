from typing import Any, Mapping
import pandas as pd
from src.config.constants import REG_FEATURE_COLUMNS
from typing import List

def reg_prepare_features(raw_input: Mapping[str, Any], required_keys:List[str]=REG_FEATURE_COLUMNS) -> pd.DataFrame:
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
    
    if not isinstance(required_keys, List):
        raise TypeError("The `required_keys` parameter must be a `List`")

    raw_input_lower = {str(k).lower(): v for k, v in raw_input.items()}
    required_keys_lower = [w.lower() for w in required_keys]

    missing = [key for key in required_keys_lower if key not in raw_input_lower]
    if missing:
        raise KeyError(f"`raw_input` is missing required keys: {missing}")

    values = [raw_input_lower[key] for key in required_keys_lower]
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