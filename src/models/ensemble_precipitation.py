"""Ensemble model for precipitation prediction."""

import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.base import BaseEstimator, RegressorMixin
from typing import Optional
import joblib


class EnsemblePrecipitationModel(BaseEstimator, RegressorMixin):
    """Ensemble model combining RF and GBM for precipitation forecasting."""

    def __init__(
        self,
        n_estimators: int = 100,
        rf_weight: float = 0.6,
        gbm_weight: float = 0.4,
        random_state: int = 42
    ):
        self.n_estimators = n_estimators
        self.rf_weight = rf_weight
        self.gbm_weight = gbm_weight
        self.random_state = random_state
        self._rf: Optional[RandomForestRegressor] = None
        self._gbm: Optional[GradientBoostingRegressor] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "EnsemblePrecipitationModel":
        """Train both ensemble components."""
        self._rf = RandomForestRegressor(
            n_estimators=self.n_estimators,
            random_state=self.random_state,
            n_jobs=-1
        )
        self._gbm = GradientBoostingRegressor(
            n_estimators=self.n_estimators,
            random_state=self.random_state
        )
        self._rf.fit(X, y)
        self._gbm.fit(X, y)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate weighted ensemble predictions."""
        if self._rf is None or self._gbm is None:
            raise ValueError("Model not fitted. Call fit() first.")
        rf_pred = self._rf.predict(X)
        gbm_pred = self._gbm.predict(X)
        return self.rf_weight * rf_pred + self.gbm_weight * gbm_pred

    def save(self, path: str) -> None:
        """Save model to disk."""
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: str) -> "EnsemblePrecipitationModel":
        """Load model from disk."""
        return joblib.load(path)
