import os
import json
import joblib
from fastapi.testclient import TestClient
from src.app import app
from src import train

client = TestClient(app)


def test_predict_endpoint():
    # Ensure a model exists by running training
    train.train_and_log()

    # Load metrics file if present
    models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
    model_path = os.path.join(models_dir, "model.pkl")
    assert os.path.exists(model_path)

    # Call predict with a sample iris vector
    sample = {"features": [5.1, 3.5, 1.4, 0.2]}
    r = client.post("/predict", json=sample)
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data


def test_report_metric_endpoint():
    r = client.post("/report_metric", json={"accuracy": 0.95})
    assert r.status_code == 200
    data = r.json()
    assert data.get("accuracy") == 0.95
