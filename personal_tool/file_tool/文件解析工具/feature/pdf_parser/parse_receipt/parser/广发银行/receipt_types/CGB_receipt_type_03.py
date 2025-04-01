from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CGB_receipt_type import CGBReceiptType
from ....entity.receipt import Receipt


class CGBReceiptType03(CGBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if {"结息帐号", "账户名称", "入息帐号", "本次计息起止日"} < set(self.table.get_col_values(0)):
            return True
        return False

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        from_date, to_date = self._get_cell_relative("^本次计息起止日$").get_value().split("-")
        receipt.date = TimeUtil.format_to_str(to_date)  # 日期
        receipt.payer_account_name = self._get_cell_relative("^账户名称$").get_value()  # 付款人户名
        receipt.payer_account_number = self._get_cell_relative("^入息帐号$").get_value()  # 付款人账号
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^实付利息总计$").get_value())  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt
