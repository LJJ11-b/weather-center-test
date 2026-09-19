"""
YAML数据加载
"""
import yaml
from config.config import TESTDATA_DIR
from utils.logger import get_logger

logger = get_logger("data")

def load_cities() -> list:
    with open(TESTDATA_DIR / "cities.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    cities = data.get("cities", [])
    logger.info(f"加载 {len(cities)} 个城市")
    return cities
