import numpy as np
import pandas as pd

from typing import Any, Mapping

REG_FEATURE_COLUMNS = [
    "Mental_Health_Status",
    "Stress_Level",
    "Work_Hours_Per_Week",
    "Screen_Time_Hours",
    "Meditation_Minutes",
    "Sleep_Hours",
    "Sleep_Quality",
    "Physical_Activity_Hours",
    "Chronic_Stress_No",
    "Chronic_Stress_Yes",
]

def reg_prepare_features(raw_input: Mapping[str, Any]) -> pd.DataFrame:
    values = [
        raw_input["mental_health"],
        raw_input["stress_level"],
        raw_input["work_hours_per_week"],
        raw_input["screen_time_hours"],
        raw_input["meditation_minutes"],
        raw_input["sleep_hours"],
        raw_input["sleep_quality"],
        raw_input["physical_activity_hours"],
        raw_input["chronic_stress_no"],
        raw_input["chronic_stress_yes"],
    ]
    return pd.DataFrame([values], columns=REG_FEATURE_COLUMNS)

def reg_predict(model,raw_input):
    features = reg_prepare_features(raw_input)
    return model.predict(features)[0]