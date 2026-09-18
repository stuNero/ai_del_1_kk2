# Imports
import io
import sqlite3
import sys
import time
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet, LassoLars, LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, cross_validate, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.tree import DecisionTreeRegressor

warnings.filterwarnings("ignore")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.paths import DB_PATH
from loaders.load_data import load_from_db

MODEL_NAME = "regression_model"


def load_and_split_data(table_name: str, test_size=0.2):
    """Load data from database and split into train/test."""

    df = load_from_db(table_name=table_name)
    y = df["Burnout_Score"]
    X = df.drop(columns="Burnout_Score")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    return X_train, X_test, y_train, y_test


def train_models(X_train, y_train):
    """Train all models and return results."""

    models_to_train = {
        "LinearRegression": {
            "pipe": make_pipeline(StandardScaler(), LinearRegression()),
            "params": {},
        },
        "LassoLars": {
            "pipe": make_pipeline(StandardScaler(), LassoLars()),
            "params": {
                "lassolars__alpha": [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
                "lassolars__max_iter": [1000, 2000],
            },
        },
        "DecisionTreeRegressor": {
            "pipe": make_pipeline(
                StandardScaler(), DecisionTreeRegressor(random_state=1337)
            ),
            "params": {
                "decisiontreeregressor__max_depth": [None, 10, 20],
                "decisiontreeregressor__max_features": ["sqrt", "log2"],
            },
        },
        "RandomForestRegressor": {
            "pipe": make_pipeline(
                StandardScaler(), RandomForestRegressor(random_state=1337)
            ),
            "params": {
                "randomforestregressor__n_estimators": [10, 50, 100],
                "randomforestregressor__max_depth": [None, 10, 20],
                "randomforestregressor__max_features": ["sqrt", "log2"],
            },
        },
        "ElasticNet": {
            "pipe": make_pipeline(StandardScaler(), ElasticNet()),
            "params": {"elasticnet__alpha": [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]},
        },
    }

    trained_models = []

    for name, config in models_to_train.items():
        print(f"Training {name}...")
        start_time = time.time()

        if name == "LinearRegression":
            cross_validate(
                config["pipe"],
                X_train,
                y_train,
                cv=5,
                n_jobs=-1,
                scoring="neg_mean_squared_error",
            )
            config["pipe"].fit(X_train, y_train)
            model = config["pipe"]

        elif config["params"]:
            model = GridSearchCV(
                config["pipe"],
                config["params"],
                cv=5,
                n_jobs=-1,
                scoring="neg_mean_squared_error",
            )
            model.fit(X_train, y_train)
        else:
            model = config["pipe"]
            model.fit(X_train, y_train)

        fit_time = time.time() - start_time

        trained_models.append({"name": name, "model": model, "fit_time": fit_time})

    return trained_models


def evaluate_models(trained_models, X_test, y_test):
    """Evaluate all models and rank by efficiency."""

    results = []

    for item in trained_models:
        preds = item["model"].predict(X_test)
        mse = mean_squared_error(y_test, preds)
        rmse = np.sqrt(mse)

        results.append(
            {
                "name": item["name"],
                "model": item["model"],
                "fit_time": item["fit_time"],
                "score": mse,
                "rmse": rmse,
            }
        )

    results_df = pd.DataFrame(results)
    results_df.sort_values("score", inplace=True)

    scaler = MinMaxScaler()
    results_df[["norm_rmse", "norm_time"]] = scaler.fit_transform(
        results_df[["rmse", "fit_time"]]
    )
    results_df["efficiency_penalty"] = results_df["norm_rmse"] + results_df["norm_time"]
    results_df = results_df.sort_values("efficiency_penalty")

    print("\n" + "=" * 70)
    print(results_df[["name", "rmse", "fit_time", "efficiency_penalty"]].to_string())
    print("=" * 70 + "\n")

    return results_df


def save_best_model_to_db(best_model, model_name, db_path=DB_PATH):
    """Save best model to database."""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            model BLOB
        )
    """)

    buffer = io.BytesIO()
    joblib.dump(best_model, buffer)
    model_bytes = buffer.getvalue()

    cursor.execute(
        "INSERT INTO models (name, model) VALUES (?,?)", (model_name, model_bytes)
    )
    conn.commit()
    conn.close()

    print(f"Model saved: {model_name}")


if __name__ == "__main__":
    # Load data
    X_train, X_test, y_train, y_test = load_and_split_data(
        table_name="burnout_data_clean"
    )

    # Train models
    trained_models = train_models(X_train, y_train)

    # Evaluate
    results_df = evaluate_models(trained_models, X_test, y_test)

    # Get best model
    best_row = results_df.iloc[0]
    best_model_obj = best_row["model"]
    best_name = best_row["name"]
    best_rmse = best_row["rmse"]

    # Retrain on full data
    best_model = (
        best_model_obj.best_estimator_
        if hasattr(best_model_obj, "best_estimator_")
        else best_model_obj
    )

    # Retrain best model on full dataset
    df = load_from_db(table_name="burnout_data_clean")
    y = df["Burnout_Score"]
    X = df.drop(columns="Burnout_Score")
    best_model.fit(X, y)

    # Save
    save_best_model_to_db(best_model, MODEL_NAME)
