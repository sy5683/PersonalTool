class Statement:

    def __init__(self):
        self.reference_number = None  # 交易流水号
        self.trade_datetime = None  # 交易时间
        self.account_name = None  # 开户名称
        self.account_number = None  # 开户账号
        self.reciprocal_account_name = None  # 对方账户名称
        self.reciprocal_account_number = None  # 对方账户号
        self.abstract = None  # 摘要
        self.purpose = None  # 用途
        self.payment_amount = 0  # 付款金额
        self.receive_amount = 0  # 收款金额
        self.balance = 0  # 余额
