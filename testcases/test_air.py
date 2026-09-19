"""
空气质量接口测试
"""
import pytest
from utils.assert_util import *
from utils.logger import get_logger

logger = get_logger("test-air")

class TestAirNow:
    def test_current_air(self, air_api, default_location):
        lat, lon = default_location
        resp = air_api.get_current(latitude=lat, longitude=lon)
        assert_http_status(resp, 200)
        assert_no_error(resp)
        now = resp.json()["current"]
        assert_has_key(now, "pm2_5")
        assert_range(now["pm2_5"], 0, 500, "PM2.5")
        logger.info(f"PM2.5={now['pm2_5']}, PM10={now['pm10']}")

    @pytest.mark.parametrize("city", [
        {"name": "北京", "lat": 39.9042, "lon": 116.4074},
        {"name": "上海", "lat": 31.2304, "lon": 121.4737},
        {"name": "海口", "lat": 20.0440, "lon": 110.1990},
    ])
    def test_multiple_cities(self, air_api, city):
        resp = air_api.get_current(latitude=city["lat"], longitude=city["lon"])
        assert_http_status(resp, 200)
        pm25 = resp.json()["current"]["pm2_5"]
        logger.info(f"{city['name']} PM2.5={pm25}")

class TestAirHourly:
    def test_hourly_air(self, air_api, default_location):
        lat, lon = default_location
        resp = air_api.get_hourly(latitude=lat, longitude=lon, forecast_days=2)
        assert_http_status(resp, 200)
        hourly = resp.json()["hourly"]
        assert_has_key(hourly, "time")
        assert_nonempty(hourly["time"], "小时数据")

class TestAirNegative:
    def test_invalid_coords(self, air_api):
        resp = air_api.get_current(latitude=999, longitude=0)
        assert resp.status_code == 400
