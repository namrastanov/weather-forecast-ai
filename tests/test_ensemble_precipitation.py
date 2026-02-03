"""Tests for ensemble precipitation model."""

import pytest
import numpy as np
from weather_forecast_ai.models.ensemble_precipitation import EnsemblePrecipitationModel


class TestEnsemblePrecipitationModel:
    """Test suite for EnsemblePrecipitationModel."""

    @pytest.fixture
    def sample_data(self):
        """Generate sample training data."""
        np.random.seed(42)
        X = np.random.randn(100, 5)
        y = np.random.rand(100) * 10
        return X, y

    @pytest.fixture
    def model(self):
        """Create model instance."""
        return EnsemblePrecipitationModel(n_estimators=10)

    def test_fit_creates_models(self, model, sample_data):
        """Test that fit initializes both sub-models."""
        X, y = sample_data
        model.fit(X, y)
        assert model._rf is not None
        assert model._gbm is not None

    def test_predict_returns_correct_shape(self, model, sample_data):
        """Test prediction output shape."""
        X, y = sample_data
        model.fit(X, y)
        predictions = model.predict(X)
        assert predictions.shape == (100,)

    def test_predict_without_fit_raises(self, model, sample_data):
        """Test that predict raises error without fit."""
        X, _ = sample_data
        with pytest.raises(ValueError):
            model.predict(X)

    def test_weights_sum_to_one(self, model):
        """Test ensemble weights."""
        assert model.rf_weight + model.gbm_weight == 1.0
