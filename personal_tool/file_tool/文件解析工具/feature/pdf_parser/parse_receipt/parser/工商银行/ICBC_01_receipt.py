import fitz

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from ...entity.receipt import Receipt
from ...entity.receipt_parser import ReceiptParser


class ICBC01Receipt(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("工商银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        with fitz.open(self.receipt_path) as pdf:
            if "www.icbc.com.cn" not in pdf[0].get_text():
                return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for table in pdf_profile.tables:
                receipt = Receipt()
                receipt.date = TimeUtil.format_time(table.get_row_values(6)[3])  # 日期
                receipt.payer_account_name = table.get_row_values(0)[2]  # 付款人户名
                receipt.payer_account_number = table.get_row_values(1)[1]  # 付款人账号
                receipt.payee_account_name = table.get_row_values(0)[5]  # 收款人户名
                receipt.payee_account_number = table.get_row_values(1)[3]  # 收款人账号
                receipt.amount = NumberUtil.to_amount(table.get_row_values(3)[1])  # 金额
                self.receipts.append(receipt)
