import fitz

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from ...entity.receipt import Receipt
from ...entity.receipt_parser import ReceiptParser


class ABC01ReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("农业银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not self._judge_images("ABC_image_01.png", different=0.3):
            return False
        with fitz.open(self.receipt_path) as pdf:
            if "网上银行电子回单" not in pdf[0].get_text():
                return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for table in pdf_profile.tables:
                receipt = Receipt()
                receipt.date = TimeUtil.format_time(table.get_row_values(7)[1])  # 日期
                name_row_values = table.get_row_values(1)
                if name_row_values[0] == "付款方":
                    receipt.payer_account_name = table.get_row_values(2)[1]  # 付款人户名
                    receipt.payer_account_number = name_row_values[2]  # 付款人账号
                    receipt.payee_account_name = table.get_row_values(2)[3]  # 收款人户名
                    receipt.payee_account_number = name_row_values[5]  # 收款人账号
                elif name_row_values[0] == "收款方":
                    receipt.payer_account_name = table.get_row_values(2)[3]  # 付款人户名
                    receipt.payer_account_number = name_row_values[5]  # 付款人账号
                    receipt.payee_account_name = table.get_row_values(2)[1]  # 收款人户名
                    receipt.payee_account_number = name_row_values[2]  # 收款人账号
                receipt.amount = NumberUtil.to_amount(table.get_row_values(4)[1])  # 金额
                self.receipts.append(receipt)
