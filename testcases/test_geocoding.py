"""
城市搜索接口测试
"""
import pytest
from utils.assert_util import *
from utils.logger import get_logger

logger = get_logger("test-geo")

class TestCitySearch:
    def test_search_chinese(self, geocoding_api):
        resp = geocoding_api.search("广州", count=5, language="zh")
        assert_http_status(resp, 200)
        results = resp.json().get("results", [])
        assert_nonempty(results, "搜索结果")
        assert_has_key(results[0], "name")
        logger.info(f"广州搜索到 {len(results)} 条")

    @pytest.mark.parametrize("city", ["北京", "上海", "深圳", "杭州", "成都", "哈尔滨"])
    def test_multiple_cities(self, geocoding_api, city):
        resp = geocoding_api.search(city, count=3)
        assert_http_status(resp, 200)
        results = resp.json().get("results", [])
        assert len(results) > 0
        logger.info(f"{city} -> {results[0]['name']}")

    def test_search_english(self, geocoding_api):
        resp = geocoding_api.search("Guangzhou", count=1, language="en")
        assert_http_status(resp, 200)
        results = resp.json().get("results", [])
        assert len(results) > 0

class TestBoundary:
    @pytest.mark.parametrize("count", [1, 10, 50])
    def test_result_count(self, geocoding_api, count):
        resp = geocoding_api.search("city", count=count)
        assert_http_status(resp, 200)
        results = resp.json().get("results", [])
        assert len(results) <= count

class TestNegative:
    def test_nonexistent(self, geocoding_api):
        resp = geocoding_api.search("xyznonexist9999", count=5)
        assert_http_status(resp, 200)
        results = resp.json().get("results", [])
        assert len(results) == 0

    def test_empty_name(self, geocoding_api):
        resp = geocoding_api.search("", count=5)
        assert resp.status_code in (200, 400)
