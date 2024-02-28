import fitz

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from ...entity.receipt import Receipt
from ...entity.receipt_parser import ReceiptParser


class CDBReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("国开行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        with fitz.open(self.receipt_path) as pdf:
            if "国家开发银行" not in pdf[0].get_text():
                return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile):
                print([each.text for each in receipt_profile.words])

            # for word in pdf_profile.words:
            #     print(word.rect)
            # for table in pdf_profile.tables:
            #     print(table.rect)
            # receipt = Receipt()
            # # print(table.get_row_values(0))
            # # if table.max_cols == 6:
            # #     pass
            # # # receipt.date = TimeUtil.format_time(table.get_row_values(7)[1])  # 日期
            # #     name_row_values = table.get_row_values(0)
            # #     if name_row_values[0] == "付款人":
            # #         receipt.payer_account_name = name_row_values[2]  # 付款人户名
            # #     #     receipt.payer_account_number = table.get_row_values(1)[]  # 付款人账号
            # #         receipt.payee_account_name = name_row_values[5]  # 收款人户名
            # #     #     receipt.payee_account_number = name_row_values[5]  # 收款人账号
            # #     elif name_row_values[0] == "收款人":
            # #         receipt.payer_account_name = name_row_values[5]  # 付款人户名
            # #     #     receipt.payer_account_number = name_row_values[5]  # 付款人账号
            # #         receipt.payee_account_name = name_row_values[2]  # 收款人户名
            # #     #     receipt.payee_account_number = name_row_values[2]  # 收款人账号
            # # # receipt.amount = NumberUtil.to_amount(table.get_row_values(4)[1])  # 金额
            # # else:
            # #     pass
            # self.receipts.append(receipt)
