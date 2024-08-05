import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .PAB_receipt_type import PABReceiptType
from ....entity.receipt import Receipt


class PABReceiptType01(PABReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not re.search("收付款业务回单|收费回单[(（]付款通知[)）]", "".join([each.text for each in self.words])):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        # 平安银行这个格式的回单间隔稍微大一点，重新合并word数据后再解析
        self.words = PdfUtil.merge_words(self.words, 40)
        receipt.date = TimeUtil.format_to_str(self._get_word("^记账日期[:：](.*?)$"))  # 日期
        receipt.receipt_number = self._get_word("^回单号[:：](.*?)$")  # 回单编号
        receipt.payer_account_name = self._get_word("^付款人名称[:：](.*?)$")  # 付款人户名
        receipt.payer_account_number = self._get_word("^付款人账号[:：](.*?)$")  # 付款人账号
        # 付款人开户银行，没有收款方时，单据只有开户行，因此这里做两层匹配
        receipt.payer_account_bank = self._get_word("^付款人开户行[:：](.*?)$") or self._get_word("^开户行[:：](.*?)$")
        receipt.payee_account_name = self._get_word("^收款人名称[:：](.*?)$")  # 收款人户名
        receipt.payee_account_number = self._get_word("^收款人账号[:：](.*?)$")  # 收款人账号
        receipt.payee_account_bank = self._get_word("^收款人开户行[:：](.*?)$")  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_word("^小写[:：](.*?)$"))  # 金额
        return receipt
