import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .CCB_receipt_type import CCBReceiptType
from ....entity.receipt import Receipt


class CCBReceiptType03(CCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.max_rows != 1 or self.table.max_cols != 1:
            return False
        if not re.search("纳税人全称及", self.table.get_row_values(0)[0]):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        words = PdfUtil.merge_words(self.table.cells[0].words, 10)
        payer_account_name_pattern = re.compile("付款人全称[:：]")
        payer_account_number_pattern = re.compile("付款人账号[:：]")
        payee_account_name_pattern = re.compile("征收机关名称[(（]委托方[)）][:：]")
        amount_pattern = re.compile("小写[(（]合计[)）]金额[:：]")
        for word in words:
            receipt.date = TimeUtil.format_to_str(self._get_word("^转账日期[:：](.*?)$"))  # 日期
            if payer_account_name_pattern.match(word.text):
                receipt.payer_account_name = payer_account_name_pattern.sub("", word.text)  # 付款人户名
            if payer_account_number_pattern.match(word.text):
                receipt.payer_account_number = payer_account_number_pattern.sub("", word.text)  # 付款人账号
            if payee_account_name_pattern.match(word.text):
                receipt.payee_account_name = payee_account_name_pattern.sub("", word.text)  # 收款人户名
            if amount_pattern.match(word.text):
                receipt.amount = NumberUtil.to_amount(amount_pattern.sub("", word.text))  # 金额
        return receipt
