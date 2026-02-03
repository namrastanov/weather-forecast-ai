"""Base class for prediction models."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional
import numpy as np
import joblib
import logging

logger = logging.getLogger(__name__)


class BasePredictionModel(ABC):
    """Abstract base class for all prediction models."""

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self._is_fitted = False
        self._metadata: dict = {}

    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray) -> "BasePredictionModel":
        """Train the model on provided data."""
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate predictions for input data."""
        pass

    def validate_input(self, X: np.ndarray) -> bool:
        """Validate input data shape and type."""
        if not isinstance(X, np.ndarray):
            raise TypeError("Input must be numpy array")
        if X.ndim != 2:
            raise ValueError("Input must be 2D array")
        return True

    def save(self, path: str) -> None:
        """Save model to disk."""
        save_path = Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        state = {
            "name": self.name,
            "version": self.version,
            "is_fitted": self._is_fitted,
            "metadata": self._metadata,
            "model_state": self._get_model_state()
        }
        joblib.dump(state, save_path)
        logger.info(f"Model saved to {save_path}")

    @classmethod
    def load(cls, path: str) -> "BasePredictionModel":
        """Load model from disk."""
        state = joblib.load(path)
        instance = cls.__new__(cls)
        instance.name = state["name"]
        instance.version = state["version"]
        instance._is_fitted = state["is_fitted"]
        instance._metadata = state["metadata"]
        instance._set_model_state(state["model_state"])
        return instance

    @abstractmethod
    def _get_model_state(self) -> dict:
        """Get internal model state for serialization."""
        pass

    @abstractmethod
    def _set_model_state(self, state: dict) -> None:
        """Restore internal model state from serialization."""
        pass

    @property
    def is_fitted(self) -> bool:
        """Check if model has been trained."""
        return self._is_fitted

    def set_metadata(self, key: str, value: Any) -> None:
        """Set model metadata."""
        self._metadata[key] = value

    def get_metadata(self, key: str) -> Optional[Any]:
        """Get model metadata."""
        return self._metadata.get(key)
