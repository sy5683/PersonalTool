import decimal


class FloatUtil:

    @staticmethod
    def add(summand: float, addend: float) -> float:
        """float加法计算"""
        return float(decimal.Decimal(str(summand)) + decimal.Decimal(str(addend)))
