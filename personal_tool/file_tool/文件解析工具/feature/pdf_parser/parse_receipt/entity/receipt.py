class Receipt:

    def __init__(self):
        self.serial_number = None  # 流水号
        self.date = None  # 日期
        self.payer_account_name = None  # 付款人户名
        self.payer_account_number = None  # 付款人账号
        self.payer_account_bank = None  # 付款人开户银行
        self.payee_account_name = None  # 收款人户名
        self.payee_account_number = None  # 收款人账号
        self.payee_account_bank = None  # 收款人开户银行
        self.amount = 0  # 金额
