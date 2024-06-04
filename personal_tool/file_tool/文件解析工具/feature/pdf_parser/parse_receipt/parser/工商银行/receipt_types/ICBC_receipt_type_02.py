import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .ICBC_receipt_type import ICBCReceiptType
from ....entity.receipt import Receipt


class ICBCReceiptType01(ICBCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not re.search("业务回单[(（]付款[)）]", "".join([each.text for each in self.words])):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self._get_word("^日期[:：](.*)$"))  # 日期
        receipt.payer_account_name = self._get_word("^付款人户名[:：](.*?)$")  # 付款人户名
        receipt.payer_account_number = self._get_word("^付款人[帐账]号[:：](.*?)$")  # 付款人账号
        receipt.payee_account_name = self._get_word("^收款人户名[:：](.*?)$")  # 收款人户名
        receipt.payee_account_number = self._get_word("^收款人[帐账]号[:：](.*?)$")  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self._get_word("^小写[:：](.*?)$"))  # 金额
        return receipt
