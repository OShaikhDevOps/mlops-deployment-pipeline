import os
import json
import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

MLFLOW_EXPERIMENT = os.environ.get("MLFLOW_EXPERIMENT", "mlops-demo")


def train_and_log():
    # Allow using a remote MLflow tracking server via MLFLOW_TRACKING_URI env var
    mlflow_uri = os.environ.get("MLFLOW_TRACKING_URI")
    if mlflow_uri:
        mlflow.set_tracking_uri(mlflow_uri)

    # Load a small dataset (replace with your dataset and DVC-tracked data)
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mlflow.set_experiment(MLFLOW_EXPERIMENT)
    with mlflow.start_run() as run:
        params = {"n_estimators": 50, "random_state": 42}
        mlflow.log_params(params)

        clf = RandomForestClassifier(**params)
        clf.fit(X_train, y_train)

        preds = clf.predict(X_test)
        acc = float(accuracy_score(y_test, preds))
        mlflow.log_metric("accuracy", acc)

        model_path = os.path.join(OUTPUT_DIR, "model.pkl")
        joblib.dump(clf, model_path)
        mlflow.log_artifact(model_path, artifact_path="model")

        # Write a small metrics file that the serving app can read to populate gauges
        metrics = {"accuracy": acc, "run_id": run.info.run_id}
        metrics_path = os.path.join(OUTPUT_DIR, "metrics.json")
        with open(metrics_path, "w") as f:
            json.dump(metrics, f)

        print(f"Run ID: {run.info.run_id}; accuracy={acc}")


if __name__ == "__main__":
    train_and_log()
