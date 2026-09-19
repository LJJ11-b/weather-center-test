"""
API请求基类
"""
import requests
from config.config import TIMEOUT
from utils.logger import get_logger

logger = get_logger("api")

class BaseApi:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def get(self, path: str, params: dict = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info(f"GET {url} | params={params}")
        try:
            resp = self.session.get(url, params=params, timeout=TIMEOUT)
            logger.info(f"响应 {resp.status_code} | {resp.elapsed.total_seconds():.3f}s")
            return resp
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {e}")
            raise
