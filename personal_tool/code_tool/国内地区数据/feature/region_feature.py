import re
import typing
from pathlib import Path

from common_util.file_util.json_util.json_util import JsonUtil
from .entity.region import RegionBase, Country
from .factory.region_factory import RegionFactory


class RegionFeature:

    @classmethod
    def get_detail_regions(cls, region_info: str) -> typing.List[RegionBase]:
        """获取详细地区数据"""
        country = cls.get_country()
        regions = []
        for province in country.provinces:
            if cls._check_by_info(province, region_info):
                regions.append(province)
            for city in province.cities:
                if cls._check_by_info(city, region_info):
                    regions.append(city)
                try:
                    for district in city.districts:
                        if cls._check_by_info(district, region_info):
                            regions.append(district)
                except AttributeError:
                    pass
        for region in regions:
            print(region.detail)
        return regions

    @classmethod
    def get_country(cls) -> Country:
        """获取国家地区数据实例化对象"""
        # 获取地区数据json数据
        region_data = JsonUtil.read_json(cls._get_region_json_path())
        # 将地区数据转换为实例化对象，以国家为单位
        return RegionFactory.data_to_country(region_data)

    @staticmethod
    def _get_region_json_path() -> Path:
        """获取地区数据文件路径"""
        # http://xzqh.mca.gov.cn/map
        return Path(__file__).parent.parent.joinpath("file/地区.json")

    @staticmethod
    def _check_by_info(region: RegionBase, region_info: str) -> bool:
        """根据地区信息判断是否为目标地区"""
        if region_info:
            if region_info.isdigit():
                if re.search(region_info, region.code):
                    return True
            else:
                if re.search(region_info, region.name):
                    return True
        return False
