"""Setup configuration for weather-forecast-ai."""

from setuptools import setup, find_packages

setup(
    name="weather-forecast-ai",
    version="0.1.0",
    description="AI-powered weather prediction service using machine learning models for accurate forecasts",
    author="Demo Author",
    author_email="demo@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "weather-forecast-ai=weather_forecast_ai.main:main",
        ],
    },
)
