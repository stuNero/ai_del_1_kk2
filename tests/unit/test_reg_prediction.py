import pytest
import re
import pandas as pd

from src.models.reg_prediction import reg_prepare_features

from src.config.constants import REG_FEATURE_COLUMNS

class TestRegPrepareFeatures:
    def test_raises_typeerror_when_raw_input_is_not_type_mapping(self):
        with pytest.raises(TypeError, match=re.escape("The `raw_input` parameter must be a `Mapping`")):
            reg_prepare_features(raw_input=["a", "b"], required_keys=["a", "b"])
    
    def test_raises_typeerror_when_required_keys_is_not_list(self):
        with pytest.raises(TypeError, match=re.escape("The `required_keys` parameter must be a `List`")):
            reg_prepare_features(raw_input={"a": "b"}, required_keys="not a list")

    def test_raises_keyerror_if_raw_input_missing_keys(self):
        with pytest.raises(KeyError, match=re.escape("`raw_input` is missing required keys:")):
            reg_prepare_features(raw_input={"a": "b"}, required_keys=["a", "b", "c"])
    
    def test_returns_single_row_dataframe_with_correct_columns_and_values(self, valid_raw_input):
        df = reg_prepare_features(raw_input=valid_raw_input)

        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] == 1
        assert df.columns.to_list() == REG_FEATURE_COLUMNS
        assert df.iloc[0].to_list() == [valid_raw_input[key] for key in REG_FEATURE_COLUMNS]

    def test_ignores_extra_keys_not_in_required_keys(self, valid_raw_input):
        raw_input_with_extra = {**valid_raw_input, "unused_key": "should be ignored"}
        df = reg_prepare_features(raw_input=raw_input_with_extra)

        assert "unused_key" not in df.columns.to_list()
        assert df.columns.to_list() == REG_FEATURE_COLUMNS

