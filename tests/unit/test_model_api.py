import pytest
import re
import sqlite3
from contextlib import closing
from src.api.model_api import fetch_model

class TestFetchModel:
    def test_raises_valueerror_when_model_type_is_invalid(self,db_path):
        with pytest.raises(ValueError, match="Invalid model type"):
            fetch_model("not a model type", db_path=db_path)

    def test_raises_valueerror_if_model_type_is_not_in_table(self,db_path):
        with closing (sqlite3.connect(db_path)) as conn:
            conn.execute(f"CREATE TABLE models (id INTEGER, name TEXT, type TEXT, model BLOB)")
        with pytest.raises(ValueError, match=re.escape("No model found with type:")):
            fetch_model("regression", db_path=db_path)
    
    def test_raises_connectionerror_if_connection_fails(self,db_path):
        with pytest.raises(ConnectionError):
            fetch_model("regression", db_path=db_path)
