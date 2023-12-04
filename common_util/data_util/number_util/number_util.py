from common_core.base.util_base import UtilBase
from .number_utils.calculate_float import CalculateFloat
from .number_utils.convert_amount import ConvertAmount


class NumberUtil(UtilBase):

    @staticmethod
    def add_float(summand: float, addend: float) -> float:
        """float加法计算"""
        return CalculateFloat.add(summand, addend)

    @staticmethod
    def divide_float(dividend: float, divisor: float) -> float:
        """float除法计算"""
        return CalculateFloat.divide(dividend, divisor)

    @staticmethod
    def multiply_float(multiplicand: float, multiplier: float) -> float:
        """float乘法计算"""
        return CalculateFloat.multiply(multiplicand, multiplier)

    @staticmethod
    def subtract_float(minuend: float, subtrahend: float) -> float:
        """float减法计算"""
        return CalculateFloat.subtract(minuend, subtrahend)

    @staticmethod
    def to_account(amount: float) -> str:
        """格式化金额，将金额数字转换为会计格式"""
        return ConvertAmount.to_account(amount)

    @staticmethod
    def to_amount(amount: any) -> float:
        """提取金额转换为浮点数"""
        return ConvertAmount.to_amount(amount)
