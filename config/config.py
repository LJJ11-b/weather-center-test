"""
全局配置
"""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

FORECAST_BASE_URL = os.getenv("FORECAST_BASE_URL", "https://api.open-meteo.com").rstrip("/")
GEOCODING_BASE_URL = os.getenv("GEOCODING_BASE_URL", "https://geocoding-api.open-meteo.com").rstrip("/")
AIR_BASE_URL = os.getenv("AIR_BASE_URL", "https://air-quality-api.open-meteo.com").rstrip("/")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
DEFAULT_LAT = float(os.getenv("DEFAULT_LAT", "23.1291"))
DEFAULT_LON = float(os.getenv("DEFAULT_LON", "113.2644"))
LOG_LEVEL = "INFO"
TESTDATA_DIR = ROOT_DIR / "testdata"
REPORTS_DIR = ROOT_DIR / "reports"
LOGS_DIR = REPORTS_DIR / "logs"
REPORTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
