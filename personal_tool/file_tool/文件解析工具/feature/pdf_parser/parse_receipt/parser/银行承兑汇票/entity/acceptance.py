from ....entity.receipt import Receipt


class Acceptance(Receipt):

    def __init__(self):
        super().__init__()
        self.due_date = None  # 汇票到期日
        self.acceptor_account_name = None  # 承兑人全称
        self.acceptor_account_number = None  # 承兑人账号
        self.acceptor_account_bank_name = None  # 承兑人开户银行名称
        self.acceptor_account_bank_number = None  # 承兑人开户银行行号
