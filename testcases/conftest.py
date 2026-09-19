"""
pytest fixtures
"""
import pytest

from api.forecast_api import ForecastApi
from api.geocoding_api import GeocodingApi
from api.air_api import AirQualityApi
from config.config import FORECAST_BASE_URL, GEOCODING_BASE_URL, AIR_BASE_URL, DEFAULT_LAT, DEFAULT_LON
from utils.data_loader import load_cities


@pytest.fixture(scope="session")
def forecast_api():
    return ForecastApi(FORECAST_BASE_URL)


@pytest.fixture(scope="session")
def geocoding_api():
    return GeocodingApi(GEOCODING_BASE_URL)


@pytest.fixture(scope="session")
def air_api():
    return AirQualityApi(AIR_BASE_URL)


@pytest.fixture(scope="session")
def cities():
    return load_cities()


@pytest.fixture(scope="session")
def default_location():
    return DEFAULT_LAT, DEFAULT_LON
