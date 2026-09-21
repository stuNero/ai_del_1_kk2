import pytest
import re
import pandas as pd

from src.models.reg_prediction import reg_prepare_features, reg_predict, process_prediction

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

class TestRegPredict:
    def test_raises_typeerror_when_model_has_no_predict_attribute(self, valid_raw_input):
        model_without_predict = object()

        with pytest.raises(TypeError, match=re.escape("The `model` parameter must implement a callable `predict` method")):
            reg_predict(model=model_without_predict, raw_input=valid_raw_input)

    def test_raises_typeerror_when_model_predict_is_not_callable(self, valid_raw_input):
        class FakeModel:
            predict = "not callable"

        with pytest.raises(TypeError, match=re.escape("The `model` parameter must implement a callable `predict` method")):
            reg_predict(model=FakeModel(), raw_input=valid_raw_input)

    def test_propagates_typeerror_when_raw_input_is_not_mapping(self, mock_model):
        with pytest.raises(TypeError, match=re.escape("The `raw_input` parameter must be a `Mapping`")):
            reg_predict(model=mock_model, raw_input=["a", "b"])

    def test_propagates_keyerror_when_raw_input_missing_keys(self, mock_model):
        with pytest.raises(KeyError, match=re.escape("`raw_input` is missing required keys:")):
            reg_predict(model=mock_model, raw_input={})

    def test_returns_rounded_prediction(self, mock_model, valid_raw_input):
        result = reg_predict(model=mock_model, raw_input=valid_raw_input)

        assert result == 4  # round(3.7, None) == 4
        assert isinstance(result, int)

    def test_calls_predict_with_prepared_features_dataframe(self, mock_model, valid_raw_input):
        reg_predict(model=mock_model, raw_input=valid_raw_input)

        called_args, _ = mock_model.predict.call_args
        features_passed = called_args[0]

        assert isinstance(features_passed, pd.DataFrame)
        assert features_passed.columns.to_list() == REG_FEATURE_COLUMNS

class TestProcessPrediction:
    
    @pytest.mark.parametrize("value", [1, "1", None, [1]])    
    def test_wrong_input_type_raises_error(self, value):
        
        with pytest.raises(TypeError):
            process_prediction(value)

    def test_returns_int(self):
        assert isinstance(process_prediction(5.5), int)

    def test_returns_zero_if_input_is_negative(self):
        assert process_prediction(-0.1) == 0

    def test_returns_hundred_if_input_is_over_hundred(self):
        assert process_prediction(100.1) == 100