import os
import json
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

MLFLOW_EXPERIMENT = os.environ.get("MLFLOW_EXPERIMENT", "mlops-demo")


def _train_with_sklearn():
    # Lazy import sklearn to avoid import-time failures when wheels are unavailable
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    params = {"n_estimators": 50, "random_state": 42}
    clf = RandomForestClassifier(**params)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = float(accuracy_score(y_test, preds))
    return clf, acc


def _train_quick_dummy():
    # Very small deterministic "model" for CI/local quick tests
    class DummyModel:
        def predict(self, X):
            # always predict class 0 (sufficient for smoke tests)
            return [0 for _ in X]

    clf = DummyModel()
    acc = 0.5
    return clf, acc


def train_and_log(quick: bool = False):
    """Train a model and log with MLflow.

    Args:
      quick: if True, use a pure-Python dummy model that requires no compiled deps.
    """
    # Allow using a remote MLflow tracking server via MLFLOW_TRACKING_URI env var
    mlflow_uri = os.environ.get("MLFLOW_TRACKING_URI")
    if mlflow_uri:
        mlflow.set_tracking_uri(mlflow_uri)

    mlflow.set_experiment(MLFLOW_EXPERIMENT)
    with mlflow.start_run() as run:
        if quick:
            clf, acc = _train_quick_dummy()
            mlflow.log_param("mode", "quick")
        else:
            clf, acc = _train_with_sklearn()
            mlflow.log_param("mode", "sklearn")

        mlflow.log_metric("accuracy", float(acc))

        model_path = os.path.join(OUTPUT_DIR, "model.pkl")
        joblib.dump(clf, model_path)
        try:
            mlflow.log_artifact(model_path, artifact_path="model")
        except Exception:
            # If MLflow artifact logging isn't configured (local file store), continue
            pass

        # Write a small metrics file that the serving app can read to populate gauges
        metrics = {"accuracy": float(acc), "run_id": run.info.run_id}
        metrics_path = os.path.join(OUTPUT_DIR, "metrics.json")
        with open(metrics_path, "w") as f:
            json.dump(metrics, f)

        print(f"Run ID: {run.info.run_id}; accuracy={acc}")


if __name__ == "__main__":
    # default to quick mode when executed directly to avoid heavy deps during quick demos
    train_and_log(quick=True)
