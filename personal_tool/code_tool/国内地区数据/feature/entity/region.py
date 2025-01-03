import typing


class RegionBase:
    """地区基类"""

    def __init__(self, code: str, name: str, detail: str = None):
        self.code = code  # 地区编码
        self.name = name  # 地区名称
        self.detail = detail if detail else name  # 详细信息

    def __str__(self) -> str:
        return f"【{self.code}】{self.name}"


class District(RegionBase):
    """区/县"""

    def __init__(self, code: str, name: str, detail: str):
        super().__init__(code, name, detail)


class City(RegionBase):
    """市"""

    def __init__(self, code: str, name: str, detail: str):
        super().__init__(code, name, detail)
        self.districts: typing.List[District] = []


class Province(RegionBase):
    """省"""

    def __init__(self, code: str, name: str):
        super().__init__(code, name)
        self.cities: typing.List[typing.Union[City, District]] = []

    def get_city(self, code: str) -> City:
        """根据编码获取对应的城市对象"""
        for city in self.cities:
            if isinstance(city, District):
                continue
            if code[:4] == city.code[:4]:
                return city


class Country(RegionBase):
    """国家"""

    def __init__(self, code: str, name: str):
        super().__init__(code, name)
        self.provinces: typing.List[Province] = []

    def get_province(self, code: str) -> Province:
        """根据编码获取对应的省份对象"""
        for province in self.provinces:
            if code[:2] == province.code[:2]:
                return province
