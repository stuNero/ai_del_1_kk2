import sqlite3
from unittest.mock import MagicMock, patch, call

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.models.reg_model_eval import (
    load_and_split_data,
    split_train_test,
    train_models,
    evaluate_models,
    get_best_model,
    final_model_train,
    save_best_model_to_db,
    run_pipeline
)
from src.config.constants import (
    REG_CLEAN_TABLE_NAME,
    REG_TARGET_COLUMN,
    REG_MODEL_TYPE
)
from src.config.paths import (
    DB_PATH
)

MODULE = "src.models.reg_model_eval"


class TestLoadAndSplitData:
    def test_splits_target_from_features(self, test_table_name, db_path):
        fake_df = pd.DataFrame({"feature_a": [1, 2, 3], "feature_b": [4, 5, 6], "target": [7, 8, 9]})

        with patch(f"{MODULE}.load_from_db", return_value=fake_df) as mock_load:
            X, y = load_and_split_data(table_name=test_table_name, target="target", db_path=db_path)

        mock_load.assert_called_once_with(table_name=test_table_name, db_path=db_path)
        assert list(X.columns) == ["feature_a", "feature_b"]
        assert "target" not in X.columns
        assert y.tolist() == [7, 8, 9]

    def test_uses_default_target_and_db_path_when_not_given(self, test_table_name):
        fake_df = pd.DataFrame({"x": [1], REG_TARGET_COLUMN: [2]})

        with patch(f"{MODULE}.load_from_db", return_value=fake_df) as mock_load:
            X, y = load_and_split_data(table_name=test_table_name)

        assert mock_load.call_args.kwargs["table_name"] == test_table_name
        assert REG_TARGET_COLUMN not in X.columns
        assert y.tolist() == [2]


class TestSplitTrainTest:
    def test_default_split_proportions(self):
        X = pd.DataFrame({"a": range(10)})
        y = pd.Series(range(10))

        X_train, X_test, y_train, y_test = split_train_test(X, y)

        assert len(X_train) == 8
        assert len(X_test) == 2
        assert len(y_train) == 8
        assert len(y_test) == 2

    def test_custom_test_size(self):
        X = pd.DataFrame({"a": range(10)})
        y = pd.Series(range(10))

        X_train, X_test, y_train, y_test = split_train_test(X, y, test_size=0.5)

        assert len(X_train) == 5
        assert len(X_test) == 5

    def test_split_is_deterministic(self):
        X = pd.DataFrame({"a": range(20)})
        y = pd.Series(range(20))

        first = split_train_test(X, y)
        second = split_train_test(X, y)

        pd.testing.assert_frame_equal(first[0], second[0])
        pd.testing.assert_frame_equal(first[1], second[1])

    def test_indices_align_between_X_and_y(self):
        X = pd.DataFrame({"a": range(10)})
        y = pd.Series(range(10))

        X_train, X_test, y_train, y_test = split_train_test(X, y)

        assert list(X_train.index) == list(y_train.index)
        assert list(X_test.index) == list(y_test.index)


class TestTrainModels:
    @pytest.fixture
    def small_data(self):
        X_train = pd.DataFrame({"f1": np.arange(20), "f2": np.arange(20) * 2})
        y_train = pd.Series(np.arange(20) * 3.0)
        return X_train, y_train

    def test_trains_all_five_models(self, small_data):
        X_train, y_train = small_data

        with patch(f"{MODULE}.GridSearchCV") as mock_gscv_cls, \
             patch(f"{MODULE}.cross_validate") as mock_cv:
            mock_gscv_cls.return_value = MagicMock()
            result = train_models(X_train, y_train)

        names = {item["name"] for item in result}
        assert names == {
            "LinearRegression",
            "LassoLars",
            "DecisionTreeRegressor",
            "RandomForestRegressor",
            "ElasticNet",
        }
        assert len(result) == 5
        for item in result:
            assert set(item.keys()) == {"name", "model", "fit_time"}
            assert isinstance(item["fit_time"], float)
            assert item["fit_time"] >= 0

    def test_linear_regression_uses_cross_validate_and_fits_directly(self, small_data):
        X_train, y_train = small_data

        with patch(f"{MODULE}.GridSearchCV") as mock_gscv_cls, \
             patch(f"{MODULE}.cross_validate") as mock_cv:
            mock_gscv_cls.return_value = MagicMock()
            result = train_models(X_train, y_train)

        mock_cv.assert_called_once()
        cv_args, cv_kwargs = mock_cv.call_args
        assert cv_kwargs["cv"] == 5
        assert cv_kwargs["scoring"] == "neg_mean_squared_error"

        lr_item = next(item for item in result if item["name"] == "LinearRegression")
        assert isinstance(lr_item["model"], Pipeline)

    def test_models_with_param_grids_use_grid_search_cv(self, small_data):
        X_train, y_train = small_data

        with patch(f"{MODULE}.GridSearchCV") as mock_gscv_cls, \
             patch(f"{MODULE}.cross_validate"):
            mock_instance = MagicMock()
            mock_gscv_cls.return_value = mock_instance
            result = train_models(X_train, y_train)

        # LassoLars, DecisionTreeRegressor, RandomForestRegressor, ElasticNet all have params
        assert mock_gscv_cls.call_count == 4
        assert mock_instance.fit.call_count == 4
        for call_args in mock_instance.fit.call_args_list:
            args, kwargs = call_args
            pd.testing.assert_frame_equal(args[0], X_train)
            pd.testing.assert_series_equal(args[1], y_train)

        grid_search_items = [item for item in result if item["name"] != "LinearRegression"]
        assert all(item["model"] is mock_instance for item in grid_search_items)


class TestEvaluateModels:
    def _make_model(self, preds):
        model = MagicMock()
        model.predict.return_value = np.array(preds)
        return model

    def test_computes_rmse_and_ranks_by_efficiency(self):
        y_test = pd.Series([1.0, 2.0, 3.0])

        trained_models = [
            {"name": "slow_accurate", "model": self._make_model([1.0, 2.0, 3.0]), "fit_time": 10.0},
            {"name": "fast_inaccurate", "model": self._make_model([5.0, 5.0, 5.0]), "fit_time": 0.1},
        ]

        results_df = evaluate_models(trained_models, pd.DataFrame({"f": [1, 2, 3]}), y_test)

        assert set(results_df["name"]) == {"slow_accurate", "fast_inaccurate"}
        assert list(results_df.columns) >= list(results_df.columns)  # columns sanity below
        for col in ["score", "rmse", "norm_rmse", "norm_time", "efficiency_penalty"]:
            assert col in results_df.columns

        # slow_accurate has perfect predictions -> rmse 0
        slow_row = results_df.set_index("name").loc["slow_accurate"]
        assert slow_row["rmse"] == pytest.approx(0.0)

        expected_mse = mean_squared_error([1.0, 2.0, 3.0], [5.0, 5.0, 5.0])
        fast_row = results_df.set_index("name").loc["fast_inaccurate"]
        assert fast_row["score"] == pytest.approx(expected_mse)
        assert fast_row["rmse"] == pytest.approx(np.sqrt(expected_mse))

    def test_results_sorted_by_efficiency_penalty(self):
        y_test = pd.Series([1.0, 2.0, 3.0])

        trained_models = [
            {"name": "worst", "model": self._make_model([10.0, 10.0, 10.0]), "fit_time": 100.0},
            {"name": "best", "model": self._make_model([1.0, 2.0, 3.0]), "fit_time": 0.01},
        ]

        results_df = evaluate_models(trained_models, pd.DataFrame({"f": [1, 2, 3]}), y_test)

        assert results_df.iloc[0]["name"] == "best"
        assert results_df.iloc[-1]["name"] == "worst"
        assert results_df["efficiency_penalty"].is_monotonic_increasing

    def test_single_model_normalizes_to_zero(self):
        y_test = pd.Series([1.0, 2.0, 3.0])
        trained_models = [
            {"name": "only_model", "model": self._make_model([1.0, 1.0, 1.0]), "fit_time": 5.0}
        ]

        results_df = evaluate_models(trained_models, pd.DataFrame({"f": [1, 2, 3]}), y_test)

        assert results_df.iloc[0]["norm_rmse"] == pytest.approx(0.0)
        assert results_df.iloc[0]["norm_time"] == pytest.approx(0.0)
        assert results_df.iloc[0]["efficiency_penalty"] == pytest.approx(0.0)


class TestGetBestModel:
    def test_returns_best_estimator_when_present(self):
        underlying_pipeline = MagicMock(name="fitted_pipeline")
        grid_search_like = MagicMock()
        grid_search_like.best_estimator_ = underlying_pipeline

        data = pd.DataFrame({"model": [grid_search_like], "score": [0.1]})

        result = get_best_model(data)

        assert result is underlying_pipeline

    def test_returns_model_directly_when_no_best_estimator(self):
        plain_pipeline = MagicMock(spec=[])  # no best_estimator_ attribute
        data = pd.DataFrame({"model": [plain_pipeline], "score": [0.1]})

        result = get_best_model(data)

        assert result is plain_pipeline

    def test_uses_first_row_of_sorted_dataframe(self):
        best = MagicMock(spec=[])
        worst = MagicMock(spec=[])
        # First row (best) should always win, regardless of extra rows below it.
        data = pd.DataFrame({"model": [best, worst], "score": [0.1, 99.0]})

        result = get_best_model(data)

        assert result is best


class TestFinalModelTrain:
    def test_calls_fit_with_full_dataset_and_returns_result(self):
        model = MagicMock()
        model.fit.return_value = "fitted_model_sentinel"
        X = pd.DataFrame({"a": [1, 2]})
        y = pd.Series([1, 2])

        result = final_model_train(model, X, y)

        model.fit.assert_called_once_with(X, y)
        assert result == "fitted_model_sentinel"


class TestSaveBestModelToDb:
    class _DummyRegressor:
        """Stand-in for a fitted sklearn estimator, used only for its class name."""
        pass

    def _make_best_model(self):
        best_model = MagicMock()
        best_model.steps = [("standardscaler", StandardScaler()), ("dummyregressor", self._DummyRegressor())]
        return best_model

    def test_creates_table_and_inserts_model(self, db_path):
        best_model = self._make_best_model()

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        with patch(f"{MODULE}.sqlite3.connect", return_value=mock_conn) as mock_connect, \
             patch(f"{MODULE}.joblib.dump") as mock_dump:
            save_best_model_to_db(best_model, model_type="Regression", db_path=db_path)

        mock_connect.assert_called_once_with(db_path)
        assert mock_cursor.execute.call_count == 2

        create_table_sql = mock_cursor.execute.call_args_list[0].args[0]
        assert "CREATE TABLE IF NOT EXISTS models" in create_table_sql

        insert_call = mock_cursor.execute.call_args_list[1]
        insert_sql, insert_params = insert_call.args
        assert "INSERT INTO models" in insert_sql
        assert insert_params[0] == "_DummyRegressor"
        assert insert_params[1] == "regression"  # lower-cased

        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_dump.assert_called_once()

    def test_wraps_db_errors_in_connection_error(self, db_path):
        best_model = self._make_best_model()

        with patch(f"{MODULE}.sqlite3.connect", side_effect=sqlite3.OperationalError("db is locked")):
            with pytest.raises(ConnectionError, match="Error saving model to database"):
                save_best_model_to_db(best_model, model_type="Regression", db_path=db_path)