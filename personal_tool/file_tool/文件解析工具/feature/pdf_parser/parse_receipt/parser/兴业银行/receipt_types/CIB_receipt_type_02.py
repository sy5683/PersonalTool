import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CIB_receipt_type import CIBReceiptType
from ....entity.receipt import Receipt


class CIBReceiptType02(CIBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not re.search("存款利息单", "".join([word.text for word in self.words])):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_word("^交易日期[:：](.*?)$"))  # 日期
        receipt.receipt_number = self._get_word("^回单编号[:：](.*?)$")  # 回单编号
        receipt.payer_account_name = self._get_word("^付款银行[:：](.*?)$")  # 付款人户名
        receipt.payee_account_name = self._get_word("^收款单位[:：](.*?)$")  # 收款人户名
        receipt.payee_account_number = self._get_word("^收款账号[:：](.*?)$")  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self._get_word("^金额[(（]小写[)）][:：](.*?)$"))  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt
