import os
import pytest
import pandas as pd
import sqlite3
import requests
import responses
from src.loaders.load_data import load_from_db, save_to_db, load_dataset
from src.config.constants import KAGGLE_DATASET_URL
# test
class TestLoadDataset:
    def test_returns_pd_dataframe(self):
        assert isinstance(load_dataset(url=KAGGLE_DATASET_URL), pd.DataFrame)
    
    @responses.activate
    def test_raises_httperror_if_faulty_url(self):
        url = "https://example.com/data.csv"
        responses.add(responses.GET, url, status=404)

        with pytest.raises(ConnectionError):
            load_dataset(url)

class TestLoadFromDb:
    def test_returns_df(self, db_with_filled_table):
        df = load_from_db(db_path=db_with_filled_table)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1

    def test_raises_when_no_tables_exist(self, db_path):
        sqlite3.connect(db_path).close()

        with pytest.raises(ConnectionError, match="no such table"):
            load_from_db(db_path=db_path)

    def test_raises_on_wrong_table_name(self, db_with_filled_table):
        with pytest.raises(ConnectionError, match="no such table"):
            load_from_db(db_path=db_with_filled_table, table_name="nonexistent_table_name")

    @pytest.mark.skipif(
        hasattr(os, "geteuid") and os.geteuid() == 0,
        reason="root bypasses filesystem permission checks",
    )
    def test_raises_on_unwritable_path(self, tmp_path):
        restricted_dir = tmp_path / "restricted"
        restricted_dir.mkdir()
        restricted_dir.chmod(0o444)  # read-only, no write/execute

        db_path = restricted_dir / "fake.db"

        with pytest.raises(ConnectionError):
            load_from_db(db_path=db_path)

    def test_returns_empty_df_when_table_has_no_rows(self, db_with_empty_table):
        df = load_from_db(db_path=db_with_empty_table)
        assert df.empty

class TestSaveToDb:
    def test_creates_table_in_database(self, db_path, one_row_df, test_table_name):
        save_to_db(df=one_row_df, db_path=db_path, table_name=test_table_name)

        conn = sqlite3.connect(db_path)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (test_table_name,)
        )
        result = cursor.fetchone()
        conn.close()

        assert result is not None

    def test_saves_correct_row_count(self, db_path, one_row_df, test_table_name):
        save_to_db(df=one_row_df, db_path=db_path, table_name=test_table_name)

        conn = sqlite3.connect(db_path)
        result_df = pd.read_sql(f"SELECT * FROM {test_table_name}", conn)
        conn.close()

        assert len(result_df) == 1

    def test_replaces_existing_table(self, db_path, one_row_df, test_table_name):
        save_to_db(df=one_row_df, db_path=db_path, table_name=test_table_name)

        new_df = pd.DataFrame({"a": [1, 2, 3]})
        save_to_db(df=new_df, db_path=db_path, table_name=test_table_name)

        conn = sqlite3.connect(db_path)
        result_df = pd.read_sql(f"SELECT * FROM {test_table_name}", conn)
        conn.close()

        assert len(result_df) == 3