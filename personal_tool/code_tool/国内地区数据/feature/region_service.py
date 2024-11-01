import typing

import flask

from common_util.interface_util.flask_util.flask_util import FlaskUtil
from .region_feature import RegionFeature


class RegionService:

    @staticmethod
    def set_route(app: flask.app):
        """设置接口"""

        # 获取详细地区数据
        @app.route("/get_detail_regions", methods=["GET", "POST"])
        def get_detail_regions() -> typing.List[str]:
            region_info = FlaskUtil.get_kwarg("region_info")
            regions = RegionFeature.get_detail_regions(region_info)
            if not regions:
                raise ValueError(f"未找到指定的地区信息: {region_info}")
            return [region.detail for region in regions]
