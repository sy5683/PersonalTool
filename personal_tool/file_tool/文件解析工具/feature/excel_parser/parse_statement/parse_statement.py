import logging
import os
from pathlib import Path

import xlrd

from common_util.code_util.import_util.import_util import ImportUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from common_util.file_util.file_util.file_util import FileUtil
from .entity.statement_parser import StatementParser


class ParseStatement:
    ImportUtil.import_modules(Path(__file__).parent.joinpath("parser"))

    @classmethod
    def parse_statement(cls, statement_path: str, **kwargs) -> StatementParser:
        """解析银行流水"""
        logging.info(f"解析银行流水: {statement_path}")
        statement_name = os.path.basename(statement_path)
        try:
            parsers = []
            for parser_class in StatementParser.__subclasses__():
                parser = parser_class(statement_path=statement_path, **kwargs)
                if parser.judge():
                    parsers.append(parser)
            if not len(parsers):
                raise ValueError(f"银行流水【{statement_name}】无法识别")
            elif len(parsers) > 1:
                raise ValueError(
                    f"银行流水【{statement_name}】匹配多种格式: %s" % "、".join([each.__str__() for each in parsers]))
            else:
                statement_parser = parsers[0]
                logging.info(f"银行流水【{statement_name}】的类型为: {statement_parser}")
                statement_parser.parse_statement()  # 调用解析流水方法
                return statement_parser
        except xlrd.XLRDError:
            # 因为财务公司的银行流水本质上是html，无法使用xlrd读取，因此当报错XLRDError时，就说明流水银行类型为财务公司
            logging.warning(f"银行流水【{statement_name}】的类型为html类型的财务公司，转换后重新处理")
            new_statement_path = ExcelUtil.xls_to_xlsx(statement_path, FileUtil.get_temp_path(statement_name))
            return cls.parse_statement(new_statement_path, **kwargs)
