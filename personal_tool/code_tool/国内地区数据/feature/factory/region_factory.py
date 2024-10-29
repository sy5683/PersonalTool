import re
import typing

from ..entity.region import Country, Province, City, District


class RegionFactory:

    @staticmethod
    def data_to_country(region_data: typing.List[typing.List[str]]) -> Country:
        """数据转国家数据对象"""
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
