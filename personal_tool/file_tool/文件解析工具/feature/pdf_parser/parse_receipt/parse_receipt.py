import logging

from common_util.file_util.pdf_util.pdf_util import PdfUtil


class ParseReceipt:

    @staticmethod
    def parse_receipt(receipt_path: str, **kwargs):
        """解析银行回单"""
        logging.info(f"解析解析银行回单: {receipt_path}")
        pdf_profiles = PdfUtil.get_pdf_profiles(receipt_path)
        for pdf_profile in pdf_profiles:
            for table in pdf_profile.tables:
                print(table.get_row_values(1))

