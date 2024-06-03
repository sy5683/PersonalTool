import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .FC_receipt_type import FCReceiptType
from ....entity.receipt import Receipt


class FCReceiptType01(FCReceiptType):

    # TODO 缺少测试文件

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return False

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        return receipt
