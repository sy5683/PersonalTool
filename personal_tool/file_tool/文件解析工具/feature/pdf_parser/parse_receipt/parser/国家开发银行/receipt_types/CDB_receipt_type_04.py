import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .CDB_receipt_type import CDBReceiptType
from ....entity.receipt import Receipt


class CDBReceiptType03(CDBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not re.search("国家开发银行电子回单", "".join([each.text for each in self.words])):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        # 国开行这个格式的回单间隔稍微大一点，重新合并word数据后再解析
        self.words = PdfUtil.merge_words(self.words, 50)
        receipt.date = TimeUtil.format_to_str(self._get_word("^交易日期[:：](.*?)$"))  # 日期
        receipt.serial_number = self._get_word("^电子回单号[(（]流水号[)）][:：](.*?)$")  # 流水号
        receipt.payer_account_name = self._get_word("^付款方名称[:：](.*?)$")  # 付款人户名
        receipt.payer_account_number = self._get_word("^付款方账号[:：](.*?)$")  # 付款人账号
        receipt.payer_account_bank = self._get_word("^付款方开户行[:：](.*?)$")  # 付款人开户银行
        receipt.payee_account_name = self._get_word("^收款方名称[:：](.*?)$")  # 收款人户名
        receipt.payee_account_number = self._get_word("^收款方账号[:：](.*?)$")  # 收款人账号
        receipt.payee_account_bank = self._get_word("^收款方开户行[:：](.*?)$")  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_word("^金额[(（]小写[)）][:：](.*?)$"))  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt
