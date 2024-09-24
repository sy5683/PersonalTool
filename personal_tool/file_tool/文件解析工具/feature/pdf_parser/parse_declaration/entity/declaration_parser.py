import abc
import typing

from .declaration import Declaration
from ...base.pdf_parser_base import PdfParserBase


class DeclarationParser(PdfParserBase, metaclass=abc.ABCMeta):
    parser_name = "申报表"

    def __init__(self, declaration_type: str, declaration_path: str, **kwargs):
        super().__init__(declaration_type, declaration_path, **kwargs)  # 申报类型
        self.declarations: typing.List[Declaration] = []
