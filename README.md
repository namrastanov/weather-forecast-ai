# weather-forecast-ai

![Python](https://img.shields.io/badge/python-3.10+-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)

AI-powered weather prediction service using machine learning models for accurate forecasts


## Features

- **ML-Powered Predictions**: Ensemble models combining Random Forest and LSTM for accurate forecasts
- **RESTful API**: FastAPI-based service with OpenAPI documentation
- **Multi-Location Support**: Forecast any location worldwide with coordinates or city name
- **Historical Analysis**: Access and analyze historical weather data
- **Caching Layer**: Redis-based caching for improved performance


## Installation

```bash
# Clone the repository
git clone https://github.com/{username}/weather-forecast-ai.git
cd weather-forecast-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Quick Start

```python
from weather_forecast_ai import main

# Initialize the application
app = main.create_app()

# Run the service
app.run()
```

## Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Key configuration options:
- `API_KEY`: Your API key for weather data providers
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis connection for caching
- `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)

## Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
ruff check .

# Format code
black .
```

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.
