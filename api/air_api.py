"""
空气质量接口
"""
from api.base_api import BaseApi

class AirQualityApi(BaseApi):
    def get_current(self, latitude, longitude, current="pm10,pm2_5,us_aqi", timezone="auto"):
        return self.get("/v1/air-quality", params={
            "latitude": latitude, "longitude": longitude,
            "current": current, "timezone": timezone,
        })

    def get_hourly(self, latitude, longitude, hourly="pm2_5,pm10,us_aqi",
                   timezone="auto", forecast_days=2):
        return self.get("/v1/air-quality", params={
            "latitude": latitude, "longitude": longitude,
            "hourly": hourly, "timezone": timezone,
            "forecast_days": forecast_days,
        })
