import pytest

from pathlib import Path
import pandas as pd

from src.loaders.load_data import ensure_dataset_exists, load_csv
from src.config.paths import DATA_PATH




def test_ensure_dataset_exists_returns_same_path():
    result = ensure_dataset_exists(csv_path=DATA_PATH)
    assert result == DATA_PATH

def test_ensure_dataset_exists_raises_for_missing_file():
    missing = Path("does_not_exist.csv")
    with pytest.raises(FileNotFoundError):
        ensure_dataset_exists(csv_path=missing)