import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .BOC_receipt_type import BOCReceiptType
from ....entity.receipt import Receipt


class BOCReceiptType01(BOCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.max_rows != 1 or self.table.max_cols != 1:
            return False
        if not re.search("国内支付业务[付收]款回单|客户[借贷]记回单|客户[付收]费回单|利息收入回单",
                         self.table.get_cell(0, 0).get_value()):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        date_pattern = re.compile("日期[:：]")
        payer_account_name_pattern = re.compile("付款人名称[:：]")
        payer_account_number_pattern = re.compile("付款人账号[:：]")
        payer_account_bank_pattern = re.compile("付款人开户行[:：]")
        payee_account_name_pattern = re.compile("收款人名称[:：]")
        payee_account_number_pattern = re.compile("收款人账号[:：]")
        payee_account_bank_pattern = re.compile("收款人开户行[:：]")
        amount_pattern = re.compile("金额[:：]")
        for word in PdfUtil.merge_words(self.table.cells[0].words, 10):
            if date_pattern.match(word.text):
                receipt.date = TimeUtil.format_to_str(date_pattern.sub("", word.text))  # 日期
            if payer_account_name_pattern.match(word.text):
                receipt.payer_account_name = payer_account_name_pattern.sub("", word.text)  # 付款人户名
            if payer_account_number_pattern.match(word.text):
                receipt.payer_account_number = payer_account_number_pattern.sub("", word.text)  # 付款人账号
            if payer_account_bank_pattern.match(word.text):
                receipt.payer_account_bank = payer_account_bank_pattern.sub("", word.text)  # 付款人开户银行
            if payee_account_name_pattern.match(word.text):
                receipt.payee_account_name = payee_account_name_pattern.sub("", word.text)  # 收款人户名
            if payee_account_number_pattern.match(word.text):
                receipt.payee_account_number = payee_account_number_pattern.sub("", word.text)  # 收款人账号
            if payee_account_bank_pattern.match(word.text):
                receipt.payee_account_bank = payee_account_bank_pattern.sub("", word.text)  # 收款人开户银行
            if amount_pattern.match(word.text):
                receipt.amount = NumberUtil.to_amount(amount_pattern.sub("", word.text))  # 金额
        return receipt
