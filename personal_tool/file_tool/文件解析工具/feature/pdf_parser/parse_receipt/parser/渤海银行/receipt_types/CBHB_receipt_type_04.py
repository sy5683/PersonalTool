import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CBHB_receipt_type import CBHBReceiptType
from ....entity.receipt import Receipt


class CBHBReceiptType04(CBHBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not re.search("客户业务回单", self.table.get_cell(0, 0).get_value()):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_cell_relative("^记账日期[:：]$").get_value())  # 日期
        receipt.receipt_number = self._get_cell_relative(r"^回单编号[:：]$").get_value()  # 回单编号
        receipt.serial_number = self._get_cell_relative(r"^记账流水[:：]$").get_value()  # 流水号
        receipt.payer_account_name = self._get_cell_relative(r"^付款方名称[:：]$").get_value()  # 付款人户名
        receipt.payer_account_number = self._get_cell_relative(r"^付款方账号[:：]$").get_value()  # 付款人账号
        receipt.payer_account_bank = self._get_cell_relative("付款方开户行[:：]$").get_value()  # 付款人开户银行
        receipt.payee_account_name = self._get_cell_relative("^收款方名称[:：]$").get_value()  # 收款人户名
        receipt.payee_account_number = self._get_cell_relative("^收款方账号[:：]$").get_value()  # 收款人账号
        receipt.payee_account_bank = self._get_cell_relative("^收款方开户行[:：]$").get_value()  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^金额[(（]小写[)）][:：]$").get_value())  # 金额
        receipt.abstract = self._get_cell_relative("^附言[:：]$").get_value()  # 摘要
        receipt.image = self.image  # 图片
        return receipt
