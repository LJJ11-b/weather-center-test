"""
城市搜索接口
"""
from api.base_api import BaseApi

class GeocodingApi(BaseApi):
    def search(self, name, count=10, language="zh"):
        return self.get("/v1/search", params={
            "name": name, "count": count, "language": language,
        })
