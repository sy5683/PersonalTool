from ....entity.voucher import Voucher


class RevenueStatement(Voucher):

    def __init__(self):
        super().__init__()
        self.transaction_number = None  # 支付宝交易号
        self.merchant_order_number = None  # 商户订单号
        self.business_type = None  # 业务类型
        self.payee_account_name = None  # 对方账户名称
        self.payee_account_number = None  # 对方支付宝账号/银行卡号
        self.revenue_balance = 0  # 收支余额
        self.account_balance = 0  # 账户余额
        self.remarks = None  # 备注
