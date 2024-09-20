import re
import typing
from pathlib import Path

from common_util.file_util.json_util.json_util import JsonUtil
from .entity.region import Country, Province, City, District


class RegionFeature:

    @classmethod
    def get_regions(cls) -> Country:
        """获取地区数据"""
        # 获取地区数据json数据
        region_data = cls._get_region_data()

        # 获取国家数据
        for code, name in region_data:
            if code == "000000":
                country = Country(code, name)
                region_data.remove([code, name])
                break
        else:
            raise ValueError("地区数据中缺少国家数据")
        # 提取省级行政区划数据
        for code, name in region_data[::]:
            if re.search("0000$", code):
                country.provinces.append(Province(code, name))
                region_data.remove([code, name])
        # 提取地级行政区划数据
        for code, name in region_data[::]:
            if re.search("00$", code):
                province = country.get_province(code)
                if province:
                    province.cities.append(City(code, name))
                    region_data.remove([code, name])
        # 提取县/区级行政区划数据
        for code, name in region_data[::]:
            province = country.get_province(code)
            city = province.get_city(code)
            if city:
                city.districts.append(District(code, name))
            else:
                province.cities.append(District(code, name))
        return country

    @staticmethod
    def _get_region_data() -> typing.List[typing.List[str]]:
        """获取地区数据json数据"""
        region_json_path = Path(__file__).parent.parent.joinpath("file\\地区.json")
        return JsonUtil.read_json(region_json_path)
