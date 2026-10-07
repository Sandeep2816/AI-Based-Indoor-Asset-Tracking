"""Lightweight ML-ready positioning model.

The default model is a RandomForest regressor when scikit-learn is installed.
For a new deployment, collect labeled RSSI samples at known floor coordinates
and train this model with train_model().
"""

import os
import pickle
import numpy as np

ANCHOR_ORDER = ["A1", "A2", "A3", "A4"]
MODEL_PATH = os.getenv("MODEL_PATH", "position_model.pkl")

try:
    from sklearn.ensemble import RandomForestRegressor
except ImportError:
    RandomForestRegressor = None

class RSSIPositionModel:
    def __init__(self):
        self.model = None

    def train(self, X, y):
        if RandomForestRegressor is None:
            raise RuntimeError("Install scikit-learn to train the ML model.")
        self.model = RandomForestRegressor(
            n_estimators=150,
            max_depth=12,
            random_state=42
        )
        self.model.fit(np.asarray(X), np.asarray(y))

    def predict(self, rssi_by_anchor):
        if self.model is None:
            return None
        vector=[float(rssi_by_anchor.get(a, -100)) for a in ANCHOR_ORDER]
        pred=self.model.predict([vector])[0]
        return round(float(pred[0]),2), round(float(pred[1]),2)

    def save(self):
        if self.model is not None:
            with open(MODEL_PATH,"wb") as f:
                pickle.dump(self.model,f)

    def load(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH,"rb") as f:
                self.model=pickle.load(f)
            return True
        return False
