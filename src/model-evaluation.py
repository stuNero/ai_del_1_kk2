# Imports
from sklearn.linear_model import LassoLars, LinearRegression, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_squared_error

import joblib
import sqlite3
import io
import pandas as pd
import numpy as np

import time
import sys
sys.path.insert(0, "../src")
from loaders.load_data import load_from_db


# ______________________________________________________________________
# Load data
df = load_from_db(table_name="burnout_data_clean")

y = df["Burnout_Score"]
X = df.drop(columns="Burnout_Score")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

lin_pipe = make_pipeline(StandardScaler(), LinearRegression())
lin_pipe.fit(X_train, y_train)

lasso_pipe = make_pipeline(StandardScaler(), LassoLars())
# lasso_pipe.fit(X_train, y_train)

tree_pipe = make_pipeline(StandardScaler(), DecisionTreeRegressor(random_state=1337))
# tree_pipe.fit(X_train, y_train)

forest_pipe = make_pipeline(StandardScaler(), RandomForestRegressor(random_state=1337))
# forest_pipe.fit(X_train, y_train)

net_pipe = make_pipeline(StandardScaler(), ElasticNet())
# net_pipe.fit(X_train, y_train)

forest_paramgrid = {
    "randomforestregressor__n_estimators": [10, 50, 100],
    "randomforestregressor__max_depth": [None, 10, 20],
    "randomforestregressor__max_features": ["sqrt", "log2"]
}

lasso_params = {
    "lassolars__alpha": [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
    "lassolars__max_iter": [1000, 2000]}

tree_paramgrid = {
    "decisiontreeregressor__max_depth": [None, 10, 20],
    "decisiontreeregressor__max_features": ["sqrt", "log2"]
}

net_params = {"elasticnet__alpha": [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]}


lin_start_time = time.time()
lin_cv = cross_validate(lin_pipe, X_train, y_train, cv=5, n_jobs=-1, scoring="neg_mean_squared_error")
lin_end_time = time.time()
lin_fit_time = lin_end_time - lin_start_time

net_start_time = time.time()
net_gs = GridSearchCV(net_pipe, net_params, cv=5, n_jobs=-1, scoring="neg_mean_squared_error")
net_gs.fit(X_train, y_train)
net_end_time = time.time()
net_fit_time = net_end_time - net_start_time

lasso_start_time = time.time()
lasso_gs = GridSearchCV(lasso_pipe, lasso_params, cv=5, n_jobs=-1, scoring="neg_mean_squared_error")
lasso_gs.fit(X_train, y_train)
lasso_end_time = time.time()
lasso_fit_time = lasso_end_time - lasso_start_time

tree_start_time = time.time()
tree_gs = GridSearchCV(tree_pipe, tree_paramgrid, cv=5, n_jobs=-1, scoring="neg_mean_squared_error")
tree_gs.fit(X_train, y_train)
tree_end_time = time.time()
tree_fit_time = tree_end_time - tree_start_time

forest_start_time = time.time()
forest_gs = GridSearchCV(forest_pipe, forest_paramgrid, cv=5, n_jobs=-1, scoring="neg_mean_squared_error")
forest_gs.fit(X_train, y_train)
forest_end_time = time.time()
forest_fit_time = forest_end_time - forest_start_time

lin_preds = lin_pipe.predict(X_test)

net_preds = net_gs.predict(X_test)
lasso_preds = lasso_gs.predict(X_test)
tree_preds = tree_gs.predict(X_test)
forest_preds = forest_gs.predict(X_test)

lin_mse = mean_squared_error(y_test, lin_preds)
net_mse = mean_squared_error(y_test, net_preds)
tree_mse = mean_squared_error(y_test, tree_preds)
forest_mse = mean_squared_error(y_test, forest_preds)
lasso_mse = mean_squared_error(y_test, lasso_preds)


models = [
    {"name": "LassoLars", "model": lasso_gs, "fit_time": lasso_fit_time, "score": lasso_mse},
    {"name": "DecisionTreeRegressor", "model": tree_gs, "fit_time": tree_fit_time, "score": tree_mse},
    {"name": "RandomForestRegressor", "model": forest_gs, "fit_time": forest_fit_time, "score": forest_mse},
    {"name": "ElasticNet", "model":net_gs, "fit_time": net_fit_time, "score": net_mse},
    {"name": "LinearRegression", "model": lin_pipe, "fit_time": lin_fit_time, "score":lin_mse}
]

models.sort(key=lambda x: x["score"])
scaler = MinMaxScaler()


model_df = pd.DataFrame(models)

model_df["rmse"] = model_df["score"] ** 0.5

model_df[["norm_rmse", "norm_time"]] = scaler.fit_transform(model_df[["rmse", "fit_time"]])

model_df["efficiency_penalty"] = model_df["norm_rmse"] + model_df["norm_time"]

model_df = model_df.sort_values("efficiency_penalty")

print(model_df[["name", "rmse", "fit_time", "efficiency_penalty"]])

best_row = model_df.iloc[0]
best_model_obj = best_row["model"]
best_model = best_model_obj.best_estimator_ if hasattr(best_model_obj, "best_estimator_") else best_model_obj

best_model.fit(X, y)

conn = sqlite3.connect("../db/burnout_database.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    model BLOB
    )
    """)

buffer = io.BytesIO()
joblib.dump(best_model, buffer)
model_bytes = buffer.getvalue()

cursor.execute(
    "INSERT INTO models (name, model) VALUES (?,?)",
    ("regression_model", model_bytes)
)
conn.commit()
conn.close()