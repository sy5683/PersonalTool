import abc

from common_util.file_util.pdf_util.pdf_util import PdfUtil


class PdfParserBase(metaclass=abc.ABCMeta):

    def __init__(self, parser_type: str, pdf_path: str, **kwargs):
        self.parser_type = parser_type  # 解析器类型
        self.pdf_profiles = PdfUtil.get_pdf_profiles(pdf_path)

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def parse(self):
        """解析"""
