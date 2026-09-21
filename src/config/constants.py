"""
constants.py

Centralized constants used across the repo: column name groups,
ordinal encoding orders, and other shared config values.

Keeping these here avoids duplicating literals across multiple
files/notebooks and keeps them in sync if columns change.
"""

# REGRESSION CONSTANS
REG_RAW_COLUMNS = [
    "Mental_Health_Status",
    "Stress_Level",
    "Chronic_Stress",
    "Work_Hours_Per_Week",
    "Screen_Time_Hours",
    "Meditation_Minutes",
    "Sleep_Hours",
    "Sleep_Quality",
    "Physical_Activity_Hours",
    "Burnout_Score",
]

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

REG_TARGET_COLUMN = "Burnout_Score"

REG_ORDINAL_COLUMNS = [
    {"name":"Mental_Health_Status", "values":["Critical", "Needs Attention", "Healthy"]},
    {"name":"Stress_Level", "values":["High", "Moderate", "Low"]},
    {"name":"Sleep_Quality", "values":["Poor", "Average", "Good", "Excellent"]},
]

REG_NOMINAL_COLUMNS = ["Chronic_Stress"]

REG_CLEAN_TABLE_NAME = "burnout_data_clean"

REG_RAW_TABLE_NAME = "burnout_data"

REG_MODEL_TYPE = "regression_model"

RANDOM_STATE = 1337