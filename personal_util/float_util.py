import decimal


class FloatUtil:

    @staticmethod
    def add_float(summand: float, addend: float) -> float:
        """float加法计算"""
        return float(decimal.Decimal(str(summand)) + decimal.Decimal(str(addend)))

    @staticmethod
    def subtract_float(minuend: float, subtrahend: float) -> float:
        """float减法计算"""
        return float(decimal.Decimal(str(minuend)) - decimal.Decimal(str(subtrahend)))

    @staticmethod
    def multiply_float(multiplicand: float, multiplier: float) -> float:
        """float乘法计算"""
        return float(decimal.Decimal(str(multiplicand)) * decimal.Decimal(str(multiplier)))

    @staticmethod
    def divide_float(dividend: float, divisor: float) -> float:
        """float除法计算"""
        if dividend == 0.0 or divisor == 0.0:
            return 0.0
        return float(decimal.Decimal(str(dividend)) / decimal.Decimal(str(divisor)))
