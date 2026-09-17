import sqlite3
import joblib
import io
from sklearn.pipeline import Pipeline

def fetch_model(model_type: str) -> Pipeline:
    """loads the model from the database and returns it
    Args: 
        model_type: The type of the model to retrieve. Valid values: 
        "regression", "classification".
    Returns:
        The deserialized sklearn estimator (or pipeline) object.
    Raises: 
        ValueError: If the model type is invalid.
        ConnectionError: If the database connection fails.
    """
    if (model_type.lower() not in ("regression","classification")):
        raise ValueError("Invalid model type")
    try:
        with sqlite3.connect("../db/burnout_database.db") as conn:
            
            cursor = conn.cursor()
            cursor.execute("SELECT model FROM models WHERE name = ?",(f"{model_type}_model",))
            row = cursor.fetchone()
            
            if row is None:
                raise ValueError(f"No model found with type: {model_type!r}")
            
            return joblib.load(io.BytesIO(row[0]))
    except sqlite3.Error as e:
        raise ConnectionError("Failed to connect to the database") from e