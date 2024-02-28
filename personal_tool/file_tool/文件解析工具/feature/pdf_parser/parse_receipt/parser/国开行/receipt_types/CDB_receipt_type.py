import abc
import re

from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import ReceiptProfile
from ....entity.receipt import Receipt


class CDBReceiptType(metaclass=abc.ABCMeta):

    def __init__(self, receipt_profile: ReceiptProfile):
        self.table = receipt_profile.table
        self.words = receipt_profile.words

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def get_receipt(self) -> Receipt:
        """解析回单"""

    def _get_date(self, pattern: str) -> str:
        for word in self.words:
            if re.search(pattern, word.text):
                return TimeUtil.format_time(re.findall(pattern, word.text)[0])
        raise ValueError("回单中无法提取到日期")
