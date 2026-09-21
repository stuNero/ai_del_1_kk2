import pytest
import re

from src.models.reg_prediction import reg_prepare_features

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