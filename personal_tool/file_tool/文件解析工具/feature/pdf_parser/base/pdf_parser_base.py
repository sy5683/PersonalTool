import abc


class PdfParserBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def parse(self):
        """解析"""
