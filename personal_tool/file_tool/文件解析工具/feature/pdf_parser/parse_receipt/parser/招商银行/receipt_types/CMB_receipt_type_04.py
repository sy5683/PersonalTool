import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .CMB_receipt_type import CMBReceiptType
from ....entity.receipt import Receipt


class CMBReceiptType03(CMBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.max_rows not in [1, 2] or self.table.max_cols != 1:
            return False
        if not re.search("出账回单", self.table.get_row_values(0)[0]):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        words = PdfUtil.merge_words(self.table.cells[0].words, 10)
        date_pattern = re.compile("交易日期[:：]")
        payer_account_name_pattern = re.compile("付款人[:：]")
        payer_account_number_pattern = re.compile("付款账号[:：]")
        amount_pattern = re.compile("交易金额[(（]小写[)）][:：]")
        for word in words:
            if date_pattern.match(word.text):
                receipt.date = TimeUtil.format_time(date_pattern.sub("", word.text))  # 日期
            if payer_account_name_pattern.match(word.text):
                receipt.payer_account_name = payer_account_name_pattern.sub("", word.text)  # 付款人户名
            if payer_account_number_pattern.match(word.text):
                receipt.payer_account_number = payer_account_number_pattern.sub("", word.text)  # 付款人账号
            if amount_pattern.match(word.text):
                receipt.amount = NumberUtil.to_amount(amount_pattern.sub("", word.text))  # 金额
        return receipt
