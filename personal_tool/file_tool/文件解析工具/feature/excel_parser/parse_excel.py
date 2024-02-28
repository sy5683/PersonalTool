import typing
from pathlib import Path

from .parse_statement.entity.statement_parser import StatementParser
from .parse_statement.parse_statement import ParseStatement


class ParseExcel:

    @staticmethod
    def parse_statement(statement_path: typing.Union[Path, str], **kwargs) -> StatementParser:
        """解析银行流水"""
        return ParseStatement.parse_statement(str(statement_path), **kwargs)
