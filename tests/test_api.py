import os
import json
import joblib
import pytest

try:
    from fastapi.testclient import TestClient
    from src.app import app
    FASTAPI_AVAILABLE = True
except Exception:
    FASTAPI_AVAILABLE = False

from src import train


def test_predict_endpoint():
    if not FASTAPI_AVAILABLE:
        pytest.skip("FastAPI not installed in this environment - skipping API tests")

    client = TestClient(app)

    # Ensure a model exists by running quick training
    train.train_and_log(quick=True)

    models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
    model_path = os.path.join(models_dir, "model.pkl")
    assert os.path.exists(model_path)

    sample = {"features": [5.1, 3.5, 1.4, 0.2]}
    r = client.post("/predict", json=sample)
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data


def test_report_metric_endpoint():
    if not FASTAPI_AVAILABLE:
        pytest.skip("FastAPI not installed in this environment - skipping API tests")

    client = TestClient(app)
    r = client.post("/report_metric", json={"accuracy": 0.95})
    assert r.status_code == 200
    data = r.json()
    assert data.get("accuracy") == 0.95
