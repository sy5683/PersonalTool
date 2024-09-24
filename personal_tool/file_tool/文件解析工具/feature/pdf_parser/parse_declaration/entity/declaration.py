class Declaration:

    def __init__(self):
        self.declaration_type = None  # 申报表类型
        self.from_date = None  # 税款所属时间起
        self.to_date = None  # 税款所属时间止
        self.revenue = 0  # 申报表收入
        self.tax_amount = 0  # 申报表税额
