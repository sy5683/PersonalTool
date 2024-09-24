from pathlib import Path

from common_util.code_util.import_util.import_util import ImportUtil
from .entity.declaration_parser import DeclarationParser
from ..base.pdf_parse_base import PdfParseBase


class ParseDeclaration(PdfParseBase):
    ImportUtil.import_modules(Path(__file__).parent.joinpath("parser"))

    @classmethod
    def parse_declaration(cls, declaration_path: str, **kwargs) -> DeclarationParser:
        """解析申报表"""
        return cls._parse(declaration_path, DeclarationParser, **kwargs)
