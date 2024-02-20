import re


class VerifyExcelData:

    @staticmethod
    def verify_scientific_notation(value: str):
        """校验科学计数法"""
        assert not re.search(r"\d+\.\d+e[+-]\d+|\.\d+e[+-]\d+", value), f"数字被自动转换为科学计数法: {value}"
