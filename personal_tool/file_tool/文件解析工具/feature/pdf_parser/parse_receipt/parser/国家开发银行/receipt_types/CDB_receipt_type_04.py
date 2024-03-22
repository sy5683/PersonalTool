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
        """解析回单"""
        receipt = Receipt()
        date_pattern = re.compile("交易日期[:：]")
        payer_account_name_pattern = re.compile("付款方名称[:：]")
        payer_account_number_pattern = re.compile("付款方账号[:：]")
        payee_account_name_pattern = re.compile("收款方名称[:：]")
        payee_account_number_pattern = re.compile("收款方账号[:：]")
        amount_pattern = re.compile("金额[(（]小写[)）][:：]")
        for word in PdfUtil.merge_words(self.words, 50):
            if date_pattern.match(word.text):
                receipt.date = TimeUtil.format_to_str(date_pattern.sub("", word.text))  # 日期
            if payer_account_name_pattern.match(word.text):
                receipt.payer_account_name = payer_account_name_pattern.sub("", word.text)  # 付款人户名
            if payer_account_number_pattern.match(word.text):
                receipt.payer_account_number = payer_account_number_pattern.sub("", word.text)  # 付款人账号
            if payee_account_name_pattern.match(word.text):
                receipt.payee_account_name = payee_account_name_pattern.sub("", word.text)  # 收款人户名
            if payee_account_number_pattern.match(word.text):
                receipt.payee_account_number = payee_account_number_pattern.sub("", word.text)  # 收款人账号
            if amount_pattern.match(word.text):
                receipt.amount = NumberUtil.to_amount(amount_pattern.sub("", word.text))  # 金额
        return receipt
