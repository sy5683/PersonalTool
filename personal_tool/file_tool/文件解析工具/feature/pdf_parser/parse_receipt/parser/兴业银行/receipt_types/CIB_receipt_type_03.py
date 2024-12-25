import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CIB_receipt_type import CIBReceiptType
from ....entity.receipt import Receipt


class CIBReceiptType03(CIBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not re.search("收费回单", self.words[1].text):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_word("^交易日期[:：](.*?)$"))  # 日期
        receipt.receipt_number = self._get_word("^回单编号[:：](.*?)$")  # 回单编号
        receipt.serial_number = self._get_word(r"业务流水号[:：]([a-zA-Z\d+]+)(.*)$")[0]  # 流水号
        receipt.payer_account_name = self._get_word("^缴费户名[:：](.*?)$")  # 付款人户名
        receipt.payer_account_number = self._get_word("^缴费账号[:：](.*?)$")  # 付款人账号
        receipt.payee_account_name = self._get_word("^收费机构[:：](.*?)$")  # 收款人户名
        receipt.amount = NumberUtil.to_amount(self._get_word("^金额[(（]小写[)）][:：](.*?)$"))  # 金额
        receipt.image = self.image  # 图片
        return receipt
