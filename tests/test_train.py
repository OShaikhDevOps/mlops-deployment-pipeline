import os
import joblib
from src import train


def test_train_creates_model(tmp_path):
    # Run training (uses sklearn iris) and confirm model is written
    train.train_and_log()
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")
    assert os.path.exists(model_path)
    # try loading the model
    clf = joblib.load(model_path)
    assert hasattr(clf, "predict")
