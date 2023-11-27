import decimal


class CalculateFloat:

    @staticmethod
    def add(summand: float, addend: float) -> float:
        """float加法计算"""
        return float(decimal.Decimal(str(summand)) + decimal.Decimal(str(addend)))

    @staticmethod
    def divide(dividend: float, divisor: float) -> float:
        """float除法计算"""
        if dividend == 0.0 or divisor == 0.0:
            return 0.0  # 当除数或被除数为0时，返回值直接为0，不然进行计算的时候会报错
        return float(decimal.Decimal(str(dividend)) / decimal.Decimal(str(divisor)))

    @staticmethod
    def multiply(multiplicand: float, multiplier: float) -> float:
        """float乘法计算"""
        return float(decimal.Decimal(str(multiplicand)) * decimal.Decimal(str(multiplier)))

    @staticmethod
    def subtract(minuend: float, subtrahend: float) -> float:
        """float减法计算"""
        # 直接相减计算float可能会出现错误，比如0.4-0.3=0.10000000000000003
        return float(decimal.Decimal(str(minuend)) - decimal.Decimal(str(subtrahend)))
