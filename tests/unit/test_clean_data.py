import pytest
import pandas as pd

from src.loaders.clean_data import reg_ordinal_encode

class TestRegOrdinalEncode():
    def test_raises_typeerror_when_values_is_not_a_list(self, one_row_df):
        with pytest.raises(TypeError):
            reg_ordinal_encode(one_row_df, column="test_column", values="not a list")
            
    def test_raises_typeerror_when_values_is_not_over_len_2(self, one_row_df):
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
        
    def test_returns_encoded_column(self, one_row_df):
        df = reg_ordinal_encode(pd.DataFrame({
            "test_column": ["medium","low","high"]}), column="test_column", values=["high", "medium", "low"])
        print(df.head())
        assert df["test_column"].iloc[0] == 1
        assert df["test_column"].iloc[1] == 2
        assert df["test_column"].iloc[2] == 0