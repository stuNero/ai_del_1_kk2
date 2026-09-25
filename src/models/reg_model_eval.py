# Imports
import io, sqlite3, time, warnings, joblib

from typing import Tuple, Dict, List, Any
import numpy as np
import pandas as pd
from pathlib import Path
from contextlib import closing

from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import ElasticNet, LassoLars, LinearRegression

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, cross_validate, train_test_split
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from src.config.paths import DB_PATH
from src.loaders.load_data import load_from_db

from src.config.constants import REG_CLEAN_TABLE_NAME, REG_TARGET_COLUMN, REG_MODEL_TYPE, RANDOM_STATE

warnings.filterwarnings("ignore")


def load_and_split_data(table_name: str, target:str=REG_TARGET_COLUMN, db_path: Path = DB_PATH) -> Tuple[pd.DataFrame, pd.Series]:
    """Load data from database and split into X and y"""

    df = load_from_db(table_name=table_name, db_path=db_path)
    y = df[target]
    X = df.drop(columns=[target])
    
    return X, y

def split_train_test(X: pd.DataFrame,  y: pd.Series, test_size:float=0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data into train/test."""

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=RANDOM_STATE)
    return X_train, X_test, y_train, y_test

def train_models(X_train :pd.DataFrame, y_train:pd.Series) -> List[Dict[str, Any]]:
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
                StandardScaler(), DecisionTreeRegressor(random_state=RANDOM_STATE)
            ),
            "params": {
                "decisiontreeregressor__max_depth": [None, 10, 20],
                "decisiontreeregressor__max_features": ["sqrt", "log2"],
            },
        },
        "RandomForestRegressor": {
            "pipe": make_pipeline(
                StandardScaler(), RandomForestRegressor(random_state=RANDOM_STATE)
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

def evaluate_models(trained_models:List[Dict[str, Any]], X_test:pd.DataFrame, y_test:pd.Series) -> pd.DataFrame:
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

def get_best_model(data:pd.DataFrame) -> Pipeline:
    """
    Gets best model from a sorted model evaluated dataframe.
    """
    best_row = data.iloc[0]
    best_model_obj = best_row["model"]

    return (
        best_model_obj.best_estimator_
        if hasattr(best_model_obj, "best_estimator_")
        else best_model_obj
    )

def final_model_train(model:Pipeline, X:pd.DataFrame, y:pd.Series) -> Pipeline:
    return model.fit(X, y)

def save_best_model_to_db(best_model:Pipeline, model_type:str, db_path:Path=DB_PATH):
    """Save best model to database."""

    try:
        with closing(sqlite3.connect(db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS models (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        type TEXT,
                        model BLOB
                    )
                """)
            buffer = io.BytesIO()
            joblib.dump(best_model, buffer)
            model_bytes = buffer.getvalue()
            
            model_name = type(best_model.steps[-1][1]).__name__
            model_type = model_type.lower()
            
            cursor.execute(
                "INSERT INTO models (name, type, model) VALUES (?,?,?)", (model_name, model_type, model_bytes)
            )
            conn.commit()
    except Exception as e:
        raise ConnectionError(f"Error saving model to database: {e}") from e
    print(f"Model saved: {model_name}, {model_type}")

def run_pipeline(db_path: Path=DB_PATH):
    # Load data
    X, y = load_and_split_data(table_name=REG_CLEAN_TABLE_NAME, target=REG_TARGET_COLUMN, db_path=db_path)
    
    # Split X and y in train and test
    X_train, X_test, y_train, y_test = split_train_test(X, y)

    # Train models
    trained_models = train_models(X_train, y_train)

    # Evaluate
    eval_results_df = evaluate_models(trained_models, X_test, y_test)

    # Get best model
    best_model = get_best_model(eval_results_df)

    # Retrain best model on full dataset
    best_model = final_model_train(best_model, X, y)

    # Save
    save_best_model_to_db(best_model=best_model, model_type=REG_MODEL_TYPE, db_path=db_path)

if __name__ == "__main__":
    run_pipeline(db_path=DB_PATH)
