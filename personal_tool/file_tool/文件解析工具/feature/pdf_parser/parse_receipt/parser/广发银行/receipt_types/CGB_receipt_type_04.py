from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CGB_receipt_type import CGBReceiptType
from ....entity.receipt import Receipt


class CGBReceiptType04(CGBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if {"交易流水号", "贷款账号", "户名", "应收利息", "应收欠息", "应收复息", "合计扣息"} <= set(
                self.table.get_col_values(0)):
            return True
        return False

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_cell_relative("^交易日期$").get_value())  # 日期
        receipt.receipt_number = self._get_word("^回单流水号[:：](.*?)$")  # 回单编号
        receipt.serial_number = self._get_cell_relative("^交易流水号$").get_value()  # 流水号
        receipt.payer_account_name = self._get_cell_relative("^户名$").get_value()  # 付款人户名
        receipt.payer_account_number = self._get_cell_relative("^贷款账号$").get_value()  # 付款人账号
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^合计扣息$").get_value())  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt
