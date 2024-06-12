import typing

import cpca


class ProcessChinese:

    @staticmethod
    def spilt_address(address: str) -> typing.Tuple[str, str, str, str]:
        """将地址分割为省、市、区、地址"""
        address_data_map = cpca.transform([address])  # 入参必须为列表，方法可以批量处理地址
        province = list(address_data_map['省'])[0]
        city = list(address_data_map['市'])[0]
        city = province if city == "市辖区" else city
        district = list(address_data_map['区'])[0]
        detailed_address = list(address_data_map['地址'])[0]
        return province, city, district, detailed_address
