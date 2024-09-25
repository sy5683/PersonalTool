import typing


class Invoice:

    def __init__(self):
        self.date = None  # 日期
        self.details: typing.List[dict] = []  # 多行明细。发票中一般都是有多行明细，且各个发票中的明细表头均不同
        self.amount = 0  # 金额
