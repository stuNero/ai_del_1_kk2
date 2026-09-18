import sys
from pathlib import Path
from typing import List

import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.constants import REG_RAW_COLUMNS
from loaders.load_data import load_from_db, save_to_db

def reg_ordinal_encode(data: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
    """
    Args:
        `data`: The **dataframe** of which a **column** will be encoded.
            Type `pd.DataFrame`
        `column`: The **column** to be encoded.
            Type `str`.
        `values`: The ordinal string **values** to encode, in order of importance from most important to least. \n
            Example: `["High", "Medium", "Low"]` -> `[0,1,2]` \n
            Type `List[str]`.
    Returns:
        A new, encoded **dataframe** (the original `data` is not modified).
    Raises:
        `TypeError`: If `values` is `None` or not a list, or has fewer than two elements.
        `TypeError`: If `data` is `None` or not a pandas DataFrame.
        `TypeError`: If `column` is `None` or not a string.
        `KeyError`: If `column` is not found in the dataframe.
        `ValueError`: If `column` in the dataframe has no rows.
    """
    if not isinstance(values, list):
        raise TypeError("The `values` parameter must be a list")
    if len(values) < 2:
        raise TypeError("The `values` parameter must be a list of at least two elements")

    if not isinstance(data, pd.DataFrame):
        raise TypeError("The `data` parameter must be a pandas DataFrame `pd.DataFrame`")

    if not isinstance(column, str):
        raise TypeError("The `column` parameter must be a string `str`")
    if column not in data.columns:
        raise KeyError(f"'{column}' is not a column in the `data` dataframe")

    if data[[column]].empty:
        raise ValueError(f"Column `{column}` in the dataframe has no rows")

    data = data.copy()
    encoder = OrdinalEncoder(categories=[values])
    data[column] = encoder.fit_transform(data[[column]])
    return data


if __name__ == "__main__":
    data = load_from_db()
    data = data[REG_RAW_COLUMNS]
    data = data.dropna()

    data = reg_ordinal_encode(data=data, column="Stress_Level", values=["High", "Moderate", "Low"])
    data = reg_ordinal_encode(data=data, column="Mental_Health_Status", values=["Critical", "Needs Attention", "Healthy"])
    data = reg_ordinal_encode(data=data, column="Sleep_Quality", values=["Poor", "Average", "Good", "Excellent"])

    data = pd.get_dummies(data, columns=["Chronic_Stress"])

    save_to_db(data, table_name="burnout_data_clean")