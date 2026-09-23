# Health tests
def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# Prediction tests
def test_prediction_returns_200(client,valid_raw_input, monkeypatch):
    monkeypatch.setattr("src.api.endpoints.reg_predict", lambda model, input:42)
    response = client.post("/prediction",json=valid_raw_input)
    assert response.status_code == 200
    assert response.json() == 42

def test_prediction_returns_integer(client,valid_raw_input, monkeypatch):
    monkeypatch.setattr("src.api.endpoints.reg_predict", lambda model, input:42)
    response = client.post("/prediction",json=valid_raw_input)
    assert type(response.json()) == int

def test_prediction_raises_httpexception_on_wrong_input(client):
    response = client.post("/prediction",json={"wrong_key":1})
    assert response.status_code == 400
    assert "missing required keys" in response.json()["detail"]