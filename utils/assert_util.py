"""
断言工具
"""
from typing import Any, Optional
from utils.logger import get_logger

logger = get_logger("assert")

def _safe_json(response) -> Optional[dict]:
    try:
        return response.json()
    except Exception:
        return None

def assert_http_status(response, expected: int = 200):
    actual = response.status_code
    assert actual == expected, f"HTTP {actual} != {expected}, url={response.url}"
    logger.info(f"状态码 {actual} OK")

def assert_no_error(response):
    data = _safe_json(response)
    assert data is not None, f"非JSON: {response.text[:200]}"
    if "error" in data:
        assert False, f"接口错误: {data['error']}"
    logger.info("接口无错误")

def assert_has_key(data: dict, key: str):
    assert key in data, f"缺少字段 {key}"
    logger.info(f"字段 {key} 存在")

def assert_type(data: dict, key: str, expected_type: type):
    assert key in data, f"缺少字段 {key}"
    assert isinstance(data[key], expected_type), f"{key} 类型错误"
    logger.info(f"字段 {key} 类型 OK")

def assert_range(value: float, lo: float, hi: float, name: str = ""):
    assert lo <= value <= hi, f"{name or '值'} {value} 超出 [{lo}, {hi}]"
    logger.info(f"{name or '值'}={value} OK")

def assert_nonempty(collection: Any, name: str = ""):
    assert len(collection) > 0, f"{name or '集合'} 为空"
    logger.info(f"{name or '集合'} 长度 {len(collection)}")
