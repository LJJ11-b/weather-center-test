"""
天气预报接口测试
"""
import pytest
from utils.assert_util import *
from utils.logger import get_logger

logger = get_logger("test-forecast")

class TestCurrentWeather:
    def test_now_basic(self, forecast_api, default_location):
        lat, lon = default_location
        resp = forecast_api.get_forecast(latitude=lat, longitude=lon,
            current="temperature_2m,wind_speed_10m,relative_humidity_2m")
        assert_http_status(resp, 200)
        assert_no_error(resp)
        now = resp.json()["current"]
        assert_has_key(now, "temperature_2m")
        assert_range(now["temperature_2m"], -90, 60, "温度")
        logger.info(f"当前温度 {now['temperature_2m']}°C")

    @pytest.mark.parametrize("city", [
        {"name": "北京", "lat": 39.9042, "lon": 116.4074},
        {"name": "上海", "lat": 31.2304, "lon": 121.4737},
        {"name": "深圳", "lat": 22.5431, "lon": 114.0579},
        {"name": "哈尔滨", "lat": 45.8038, "lon": 126.5349},
    ])
    def test_multiple_cities(self, forecast_api, city):
        resp = forecast_api.get_forecast(latitude=city["lat"], longitude=city["lon"], current="temperature_2m")
        assert_http_status(resp, 200)
        temp = resp.json()["current"]["temperature_2m"]
        logger.info(f"{city['name']} {temp}°C")

    @pytest.mark.parametrize("unit, range_", [("celsius", (-90, 60)), ("fahrenheit", (-130, 140))])
    def test_temperature_unit(self, forecast_api, default_location, unit, range_):
        lat, lon = default_location
        resp = forecast_api.get_forecast(latitude=lat, longitude=lon,
            current="temperature_2m", temperature_unit=unit)
        assert_http_status(resp, 200)
        temp = resp.json()["current"]["temperature_2m"]
        assert_range(temp, *range_, f"温度({unit})")

class TestDailyForecast:
    def test_3d(self, forecast_api, default_location):
        lat, lon = default_location
        resp = forecast_api.get_forecast(latitude=lat, longitude=lon,
            daily="temperature_2m_max,temperature_2m_min", forecast_days=3)
        assert_http_status(resp, 200)
        daily = resp.json()["daily"]
        assert len(daily["time"]) == 3

    def test_7d(self, forecast_api, default_location):
        lat, lon = default_location
        resp = forecast_api.get_forecast(latitude=lat, longitude=lon,
            daily="temperature_2m_max,sunrise,sunset", forecast_days=7)
        assert_http_status(resp, 200)
        daily = resp.json()["daily"]
        assert len(daily["time"]) == 7

    @pytest.mark.parametrize("days", [1, 7, 16])
    def test_days_boundary(self, forecast_api, default_location, days):
        lat, lon = default_location
        resp = forecast_api.get_forecast(latitude=lat, longitude=lon,
            daily="temperature_2m_max", forecast_days=days)
        assert_http_status(resp, 200)
        times = resp.json()["daily"]["time"]
        assert len(times) == days

class TestHourlyForecast:
    def test_24h(self, forecast_api, default_location):
        lat, lon = default_location
        resp = forecast_api.get_forecast(latitude=lat, longitude=lon,
            hourly="temperature_2m,relative_humidity_2m", forecast_days=1)
        assert_http_status(resp, 200)
        hourly = resp.json()["hourly"]
        assert_nonempty(hourly["time"], "小时数据")

    def test_3d_hourly(self, forecast_api, default_location):
        lat, lon = default_location
        resp = forecast_api.get_forecast(latitude=lat, longitude=lon,
            hourly="temperature_2m", forecast_days=3)
        assert_http_status(resp, 200)
        times = resp.json()["hourly"]["time"]
        assert 60 <= len(times) <= 80, f"3天应约72小时，实际{len(times)}"

class TestBoundary:
    @pytest.mark.parametrize("lat, lon, should_pass", [
        (90, 0, True), (-90, 0, True), (0, 180, True), (0, -180, True),
        (90.1, 0, False), (-90.1, 0, False), (0, 180.1, False),
    ])
    def test_coordinate(self, forecast_api, lat, lon, should_pass):
        resp = forecast_api.get_forecast(latitude=lat, longitude=lon, current="temperature_2m")
        if should_pass:
            assert_http_status(resp, 200)
        else:
            assert resp.status_code == 400, f"({lat},{lon})应400，实际{resp.status_code}"

class TestNegative:
    def test_invalid_variable(self, forecast_api, default_location):
        lat, lon = default_location
        resp = forecast_api.get_forecast(latitude=lat, longitude=lon, current="nonexistent_var")
        assert resp.status_code in (200, 400)

    def test_wrong_type(self, forecast_api):
        resp = forecast_api.get_forecast(latitude="abc", longitude=113)
        assert resp.status_code == 400
