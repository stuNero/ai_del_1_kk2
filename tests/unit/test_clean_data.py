import pytest
import pandas as pd
import numpy as np
import re

from src.loaders.clean_data import reg_ordinal_encode, prune_data, reg_nominal_encode

class TestRegOrdinalEncode():
    def test_raises_typeerror_when_values_is_not_a_list(self, one_row_df):
        with pytest.raises(TypeError):
            reg_ordinal_encode(one_row_df, column="test_column", values="not a list")
            
    def test_raises_typeerror_when_values_is_not_over_len_2(self):
        with pytest.raises(TypeError):
            reg_ordinal_encode(data=pd.DataFrame({"test_column": [1, 2]}), column="test_column", values=[1])
            
    def test_raises_typeerror_when_data_is_not_type_pd_dataframe(self):
        with pytest.raises(TypeError):
            reg_ordinal_encode("not a dataframe", "test_column", values=[1,2,3])
            
    def test_raises_typeerror_when_column_is_not_type_str(self, one_row_df):
        with pytest.raises(TypeError):
            reg_ordinal_encode(one_row_df, 1, values=[1,2,3])
            
    def test_raises_keyerror_when_column_not_in_data(self, one_row_df):
        with pytest.raises(KeyError):
            reg_ordinal_encode(one_row_df, "test_column", values=[1,2,3])
            
    def test_raises_valueerror_when_column_is_empty(self):
        with pytest.raises(ValueError):
            reg_ordinal_encode(pd.DataFrame({"test_column": []}), "test_column", values=[1,2])
    
    def test_returns_pd_dataframe(self):
        df = reg_ordinal_encode(pd.DataFrame({"test_column": [1,2]}), "test_column", values=[1,2])
        assert isinstance(df, pd.DataFrame)
        
    def test_returns_encoded_column(self):
        df = reg_ordinal_encode(pd.DataFrame({
            "test_column": ["medium","low","high"]}), column="test_column", values=["high", "medium", "low"])
        print(df.head())
        assert df["test_column"].iloc[0] == 1
        assert df["test_column"].iloc[1] == 2
        assert df["test_column"].iloc[2] == 0

class TestPruneData:
    def test_raises_typeerror_when_data_is_not_type_pd_dataframe(self):
        with pytest.raises(TypeError, match="The `data` parameter must be a pandas DataFrame `pd.DataFrame`"):
            prune_data("not a dataframe", ["test_column"])
    
    def test_raises_typerror_when_columns_not_type_list(self):
        with pytest.raises(TypeError, match="The `columns` parameter must be a list"):
            prune_data(data=pd.DataFrame({"test_column": [1,2]}), columns="test_column")
    
    def test_raises_valueerror_when_columns_is_empty_list(self):
        with pytest.raises(ValueError, match="The `columns` parameter must be a non-empty list"):
            prune_data(data=pd.DataFrame({"test_column": [1,2]}), columns=[])

    def test_raises_keyerror_when_column_not_in_df(self):
        with pytest.raises(KeyError, match=re.escape("Column(s) not found in the `data` dataframe:")):
            prune_data(data=pd.DataFrame({"test_column": [1,2]}), columns=["test_column", "not_in_df"])

    def test_raises_valueerror_on_empty_dataframe(self):
        with pytest.raises(ValueError, match="The `data` dataframe has no rows"):
            prune_data(data=pd.DataFrame({}), columns=["test_column"])

    def test_returns_pd_dataframe(self):
        assert isinstance(prune_data(data=pd.DataFrame({"test_column": [1,2]}), columns=["test_column"]), pd.DataFrame)
    
    def test_returns_pd_dataframe_with_pruned_columns(self):
        df = prune_data(data=pd.DataFrame({"test_column": [1,2], "test_column_2":[1,2]}), columns=["test_column"])
        assert df.shape == (2, 1)
        column_in_list = False
        if "test_column_2" in df.columns.to_list():
            column_in_list = True
        assert column_in_list == False
    
    def test_returns_pd_dataframe_without_na_values(self):
        df = prune_data(data=pd.DataFrame({"test_column": [1,np.nan], "test_column_2":[1,2]}), columns=["test_column"])
        assert int(df.isnull().sum().iloc[0]) == 0

class TestNominalEncode:
    def test_raises_typeerror_when_data_is_not_type_pd_dataframe(self):
        with pytest.raises(TypeError, match="The `data` parameter must be a pandas DataFrame `pd.DataFrame`"):
            reg_nominal_encode("not a dataframe", ["test_column"])
        
    def test_raises_typeerror_when_column_is_not_list(self):
        with pytest.raises(TypeError, match="The `columns` parameter must be a list"):
            reg_nominal_encode(pd.DataFrame({"test_column": [1,2,3]}), "test_column")
    
    def test_raises_valueerror_when_columns_is_empty(self):
        with pytest.raises(ValueError, match="The `columns` parameter must be a non-empty list"):
            reg_nominal_encode(pd.DataFrame({"test_column": [1,2,3]}), [])

    def test_raises_keyerror_when_column_is_not_in_dataframe(self):
        with pytest.raises(KeyError, match=re.escape("Column(s) not found in the `data` dataframe: ")):
            reg_nominal_encode(pd.DataFrame({"test_column": [1,2,3]}), ["not_a_column"])

    def test_raises_valueerror_if_dataframe_is_empty(self):
        with pytest.raises(ValueError, match="The `data` dataframe has no rows"):
            reg_nominal_encode(pd.DataFrame({}), ["test_column"])

    def test_returns_pd_dataframe(self):
        df = reg_nominal_encode(pd.DataFrame({"test_column": ["test_value_1","test_value_2","test_value_3"]}), ["test_column"])
        assert isinstance(df, pd.DataFrame)
    
    def test_returns_pd_dataframe_with_nominal_columns(self):
        df = reg_nominal_encode(pd.DataFrame({"test_column": ["test_value_1","test_value_2","test_value_3"]}), ["test_column"])
        expected = ["test_column_test_value_1", "test_column_test_value_2", "test_column_test_value_3"]
        assert all(col in df.columns.to_list() for col in expected)