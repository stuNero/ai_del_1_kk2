from typing import List

import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

from src.config.constants import REG_RAW_COLUMNS, REG_ORDINAL_COLUMNS, REG_NOMINAL_COLUMNS, REG_CLEAN_TABLE_NAME, REG_RAW_TABLE_NAME
from src.loaders.load_data import load_from_db, save_to_db

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

def prune_data(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Prune the columns in the dataframe `data` to only the columns in the list `columns`.
    And drop rows with missing values.
    Args:
        `data`: The **dataframe** to prune columns from.
            Type `pd.DataFrame`.
        `columns`: The list of **columns** to keep in the dataframe.
            Type `List[str]`.
    Returns:
        A new, pruned **dataframe** (the original `data` is not modified).
    Raises:
        `TypeError`: If `data` is `None` or not a pandas DataFrame.
        `TypeError`: If `columns` is `None` or not a list, or is empty.
        `KeyError`: If any column in `columns` is not found in the dataframe.
        `ValueError`: If the dataframe has no rows.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The `data` parameter must be a pandas DataFrame `pd.DataFrame`")

    if not isinstance(columns, list):
        raise TypeError("The `columns` parameter must be a list")
    if len(columns) < 1:
        raise TypeError("The `columns` parameter must be a non-empty list")

    missing = [col for col in columns if col not in data.columns]
    if missing:
        raise KeyError(f"Column(s) not found in the `data` dataframe: {missing}")

    if data.empty:
        raise ValueError("The `data` dataframe has no rows")

    data = data.copy()
    data = data[columns]
    data = data.dropna()
    return data


def reg_nominal_encode(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    One-hot encode the given nominal columns in `data`.
    Args:
        `data`: The **dataframe** to encode.
            Type `pd.DataFrame`.
        `columns`: The list of nominal **columns** to one-hot encode.
            Type `List[str]`.
    Returns:
        A new, encoded **dataframe** (the original `data` is not modified).
    Raises:
        `TypeError`: If `data` is `None` or not a pandas DataFrame.
        `TypeError`: If `columns` is `None` or not a list, or is empty.
        `KeyError`: If any column in `columns` is not found in the dataframe.
        `ValueError`: If the dataframe has no rows.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The `data` parameter must be a pandas DataFrame `pd.DataFrame`")

    if not isinstance(columns, list):
        raise TypeError("The `columns` parameter must be a list")
    if len(columns) < 1:
        raise TypeError("The `columns` parameter must be a non-empty list")

    missing = [col for col in columns if col not in data.columns]
    if missing:
        raise KeyError(f"Column(s) not found in the `data` dataframe: {missing}")

    if data.empty:
        raise ValueError("The `data` dataframe has no rows")

    data = data.copy()
    return pd.get_dummies(data, columns=columns)

def run_pipeline():
    df = load_from_db(table_name=REG_RAW_TABLE_NAME)

    df = prune_data(df, REG_RAW_COLUMNS)
    
    for ordinal_column in REG_ORDINAL_COLUMNS:
        df = reg_ordinal_encode(df, ordinal_column["name"], ordinal_column["values"])

    df = reg_nominal_encode(df, columns=REG_NOMINAL_COLUMNS)
    
    save_to_db(df, table_name=REG_CLEAN_TABLE_NAME)
    

if __name__ == "__main__":
    run_pipeline()