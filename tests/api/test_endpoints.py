from fastapi.testclient import TestClient
from fastapi import HTTPException
from src.api.endpoints import app
import pytest

client = TestClient(app)

def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_prediction_returns_200(valid_raw_input, monkeypatch):
    monkeypatch.setattr("src.api.endpoints.reg_predict", lambda model, input:42)
    response = client.post("/prediction",json=valid_raw_input)
    assert response.status_code == 200
    assert response.json() == 42

def test_prediction_returns_integer(valid_raw_input):
    response = client.post("/prediction",json=valid_raw_input)
    assert type(response.json()) == int

def test_prediction_raises_httpexception_on_wrong_input():
    response = client.post("/prediction",json={"wrong_key":1})
    assert response.status_code == 400
    assert "missing required keys" in response.json()["detail"]