import re


class ConvertAmount:

    @staticmethod
    def to_account(amount: float) -> str:
        """格式化金额，将金额数字转换为会计格式"""
        if amount is None:
            amount = 0.0
        try:
            return "{:,.2f}".format(float(amount))
        except ValueError:
            raise ValueError(f"金额异常: {amount}")

    @classmethod
    def to_amount(cls, amount: any) -> float:
        """提取金额转换为浮点数"""
        amount_str = cls._get_amount_str(amount)
        if not amount_str or amount_str == "-":
            return 0.0
        try:
            return cls._round_amount(float(amount_str))
        except ValueError:
            raise ValueError(f"金额异常: {amount_str}")

    @staticmethod
    def _get_amount_str(amount: any) -> str:
        """提取金额中的目标字符串"""
        amount_str = ""
        for each in re.findall(r"^-|\d+|\.+", str(amount)):
            amount_str += each
        return amount_str

    @staticmethod
    def _round_amount(amount: float) -> float:
        """国际统一标准金额保留两位小数"""
        return round(amount, ndigits=2)
