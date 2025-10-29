import os
import json
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl"))

app = FastAPI(title="mlops-deployment-pipeline - model serving")

pred_counter = Counter("prediction_requests_total", "Total number of prediction requests")
last_accuracy = Gauge("last_model_accuracy", "Last known model accuracy (if reported by training)")

class PredictRequest(BaseModel):
    features: List[float]

model = None


def load_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run training first.")
        model = joblib.load(MODEL_PATH)
    return model


def load_metrics():
    metrics_path = os.path.join(os.path.dirname(__file__), "..", "models", "metrics.json")
    metrics_path = os.path.abspath(metrics_path)
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    pred_counter.inc()
    try:
        clf = load_model()
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    X = [req.features]
    pred = clf.predict(X).tolist()
    return {"prediction": pred}


@app.get("/metrics")
def metrics():
    # Expose prometheus metrics
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.post("/report_metric")
def report_metric(payload: dict):
    """Allow CI/training to push a small metrics payload (e.g., accuracy) to update gauges."""
    if "accuracy" in payload:
        try:
            val = float(payload["accuracy"])
            last_accuracy.set(val)
            # persist to models/metrics.json so restarts pick it up
            metrics_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "metrics.json"))
            os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
            with open(metrics_path, "w") as f:
                json.dump({"accuracy": val}, f)
            return {"status": "ok", "accuracy": val}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="payload must include 'accuracy'")
