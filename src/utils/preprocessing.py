"""Data preprocessing utilities."""

import numpy as np
import pandas as pd
from typing import Tuple, Optional
from sklearn.preprocessing import StandardScaler, MinMaxScaler


class WeatherDataPreprocessor:
    """Preprocessor for weather time series data."""

    def __init__(self, scaling_method: str = "standard"):
        self.scaling_method = scaling_method
        self._scaler = None
        self._feature_names: list = []

    def fit_transform(
        self,
        df: pd.DataFrame,
        target_col: str = "temperature"
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Fit scaler and transform data."""
        self._feature_names = [c for c in df.columns if c != target_col]
        
        if self.scaling_method == "standard":
            self._scaler = StandardScaler()
        else:
            self._scaler = MinMaxScaler()
        
        X = df[self._feature_names].values
        y = df[target_col].values
        
        X_scaled = self._scaler.fit_transform(X)
        return X_scaled, y

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Transform new data using fitted scaler."""
        if self._scaler is None:
            raise ValueError("Preprocessor not fitted")
        return self._scaler.transform(df[self._feature_names].values)

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """Inverse transform scaled data."""
        if self._scaler is None:
            raise ValueError("Preprocessor not fitted")
        return self._scaler.inverse_transform(X)


def add_time_features(df: pd.DataFrame, datetime_col: str = "datetime") -> pd.DataFrame:
    """Add cyclical time features to dataframe."""
    df = df.copy()
    dt = pd.to_datetime(df[datetime_col])
    
    df["hour_sin"] = np.sin(2 * np.pi * dt.dt.hour / 24)
    df["hour_cos"] = np.cos(2 * np.pi * dt.dt.hour / 24)
    df["day_sin"] = np.sin(2 * np.pi * dt.dt.dayofyear / 365)
    df["day_cos"] = np.cos(2 * np.pi * dt.dt.dayofyear / 365)
    
    return df
