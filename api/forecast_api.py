"""
天气预报接口
"""
from api.base_api import BaseApi

class ForecastApi(BaseApi):
    def get_forecast(self, latitude, longitude, current=None, hourly=None, daily=None,
                     timezone="auto", temperature_unit="celsius", forecast_days=7, **extra):
        params = {
            "latitude": latitude, "longitude": longitude,
            "timezone": timezone, "temperature_unit": temperature_unit,
            "forecast_days": forecast_days,
        }
        if current: params["current"] = current
        if hourly: params["hourly"] = hourly
        if daily: params["daily"] = daily
        params.update(extra)
        return self.get("/v1/forecast", params=params)
