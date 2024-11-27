import typing

import flask
import flask_cors

from common_util.interface_util.flask_util.flask_util import FlaskUtil
from .region_feature import RegionFeature


class RegionService:
    service_name = "region_service"

    @classmethod
    def set_route(cls, app: flask.app):
        """设置接口"""

        # 获取详细地区数据
        @app.route(f"/{cls.service_name}/get_detail_regions", methods=["GET", "POST"])
        @flask_cors.cross_origin()
        def get_detail_regions() -> typing.List[str]:
            region_info = FlaskUtil.get_kwarg("region_info")
            regions = RegionFeature.get_detail_regions(region_info)
            if not regions:
                raise ValueError(f"未找到指定的地区信息: {region_info}")
            return [region.detail for region in regions]
