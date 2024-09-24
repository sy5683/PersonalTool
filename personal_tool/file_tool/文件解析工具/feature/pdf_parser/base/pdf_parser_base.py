import abc
import re

import fitz

from common_util.file_util.pdf_util.pdf_util import PdfUtil


class PdfParserBase(metaclass=abc.ABCMeta):

    def __init__(self, parser_type: str, pdf_path: str, **kwargs):
        self.parser_type = parser_type  # 解析器类型
        self.pdf_path = pdf_path  # 文件路径
        self.pdf_profiles = PdfUtil.get_pdf_profiles(pdf_path, **kwargs)

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def parse(self):
        """解析"""

    def _check_contains(self, *values: str) -> bool:
        """判断pdf中是否包含"""
        with fitz.open(self.pdf_path) as pdf:
            pdf_text = re.sub(r"\s+", "", pdf[0].get_text())
            for value in values:
                if value in pdf_text:
                    return True
        return False
