import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CBHB_receipt_type import CBHBReceiptType
from ....entity.receipt import Receipt


class CBHBReceiptType03(CBHBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not re.search("小额来账贷记凭证|大额来账一般支付凭证", self.table.get_cell(0, 0).get_value()):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self._get_cell_relative("^委托日期[:：]$").get_value())  # 日期
        receipt.serial_number = self._get_cell_relative(r"^支付系统流水号[:：]$").get_value()  # 流水号
        receipt.payer_account_name = self._get_cell_relative(r"^付款人名称[:：]$").get_value()  # 付款人户名
        receipt.payer_account_number = self._get_cell_relative(r"^付款人账号[:：]$").get_value()  # 付款人账号
        receipt.payer_account_bank = self._get_cell_relative("发起行名称[:：]$").get_value()  # 付款人开户银行
        receipt.payee_account_name = self._get_cell_relative("^收款人名称[:：]$").get_value()  # 收款人户名
        receipt.payee_account_number = self._get_cell_relative("^收款人账号[:：]$").get_value()  # 收款人账号
        receipt.payee_account_bank = self._get_cell_relative("^接收行名称[:：]$").get_value()  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^小写金额[:：]$").get_value())  # 金额
        return receipt
