import pandas as pd
import sys

from sklearn.preprocessing import OrdinalEncoder
sys.path.insert(0, "../src")

from load_data import load_from_db, save_to_db

data = load_from_db()

columns = [
    "Mental_Health_Status",
    "Stress_Level",
    "Chronic_Stress",
    "Work_Hours_Per_Week",
    "Screen_Time_Hours",
    "Meditation_Minutes",
    "Sleep_Hours",
    "Sleep_Quality",
    "Physical_Activity_Hours",
    "Burnout_Score"
]

data = data[columns]

data = data.dropna()

stress_lvl_encoder = OrdinalEncoder(categories=[["High", "Moderate", "Low"]])

mental_health_status_encoder = OrdinalEncoder(categories=[["Critical", "Needs Attention", "Healthy"]])

sleep_quality_encoder = OrdinalEncoder(categories=[["Poor", "Average", "Good", "Excellent"]])

data["Stress_Level"] = stress_lvl_encoder.fit_transform(data[["Stress_Level"]])

data["Mental_Health_Status"] = mental_health_status_encoder.fit_transform(data[["Mental_Health_Status"]])

data["Sleep_Quality"] = sleep_quality_encoder.fit_transform(data[["Sleep_Quality"]])

data = pd.get_dummies(data, columns=["Chronic_Stress"])

save_to_db(data, table_name="burnout_data_clean")