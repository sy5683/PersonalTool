from ....entity.voucher import Voucher


class SettlementRecord(Voucher):

    def __init__(self):
        super().__init__()
        self.order_amount = None  # 订单金额(元)
        self.order_quantity = None  # 订单笔数
        self.refund_amount = None  # 退款金额(元)
        self.refund_quantity = None  # 退款笔数
        self.commission = None  # 手续费(元)
        self.entry_amount = None  # 入账金额(元)
