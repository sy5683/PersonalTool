class Receipt:

    def __init__(self):
        self.type = None  # 类型
        self.bank = None  # 银行
        self.pay_type = None  # 收付类型
        self.receipt_account_name = None  # 回单户名
        self.receipt_account_number = None  # 回单账号
        self.date = None  # 日期
        self.receipt_number = None  # 回单编号
        self.serial_number = None  # 流水号
        self.payer_account_name = None  # 付款人户名
        self.payer_account_number = None  # 付款人账号
        self.payer_account_bank = None  # 付款人开户银行
        self.payee_account_name = None  # 收款人户名
        self.payee_account_number = None  # 收款人账号
        self.payee_account_bank = None  # 收款人开户银行
        self.amount = 0  # 金额
        self.abstract = None  # 摘要
        self.image = None  # 图片

    def __str__(self) -> str:
        return self.type
