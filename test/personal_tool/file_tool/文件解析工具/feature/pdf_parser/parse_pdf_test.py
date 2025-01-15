import re
import typing
from pathlib import Path

from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from personal_tool.file_tool.文件解析工具.feature.pdf_parser.parse_pdf import ParsePdf


class ParsePdfTestCase(TestBase):

    def setUp(self):
        self.declaration_path = Path(r"E:\Document\公司文档\RPA\场景文档\28_公文机器人\05-收入核对\申报表")
        self.invoice_path = Path(r"E:\Document\公司文档\RPA\场景文档\21_制单机器人\4制单机器人_税费缴纳")
        self.receipt_path = Path(r"E:\Document\公司文档\RPA\场景文档\01_银行回单补扫\回单")
        self.voucher_path = Path(r"E:\Document\公司文档\RPA\场景文档\云驿燃料调运平台场景\电子凭证")

    def test_parse_declaration(self):
        for declaration_path in self.__get_pdf_path(self.declaration_path.joinpath("")):
            parser = ParsePdf.parse_declaration(declaration_path)
            for declaration in parser.declarations:
                print(declaration.__dict__)

    def test_parse_invoice(self):
        for invoice_path in self.__get_pdf_path(self.invoice_path.joinpath(r"")):
            parser = ParsePdf.parse_invoice(invoice_path)
            for receipt in parser.invoices:
                print(receipt.__dict__)

    def test_parse_receipt(self):
        for receipt_path in self.__get_pdf_path(self.receipt_path.joinpath(r"")):
            parser = ParsePdf.parse_receipt(receipt_path)
            for receipt in parser.receipts:
                # image_path = f"E:\\{receipt}.png"
                # import os
                # if not os.path.exists(image_path):
                #     from common_util.file_util.image_util.image_util import ImageUtil
                #     ImageUtil.save_opencv_image(receipt.image, image_path)
                receipt.image = None  # 为了便于测试查看，去除图片数据
                ObjectUtil.print_object(receipt)

    def test_parse_voucher(self):
        for voucher_path in self.__get_pdf_path(self.voucher_path.joinpath(r"")):
            parser = ParsePdf.parse_voucher(voucher_path)
            for voucher in parser.vouchers:
                print(voucher.__dict__)

    @staticmethod
    def __get_pdf_path(pdf_path: Path) -> typing.List[Path]:
        return [each for each in pdf_path.rglob("*") if re.search("pdf|xps", each.suffix.lower())]
