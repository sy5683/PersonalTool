import logging
import os.path
import typing
from pathlib import Path

import xlrd

from common_util.code_util.import_util.import_util import ImportUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from common_util.file_util.file_util.file_util import FileUtil
from .entity.statement_profile import StatementProfile


class ParseStatement:
    ImportUtil.import_modules(Path(__file__).parent.joinpath("profiles"))

    @classmethod
    def parse_statement(cls, statement_path: str, **kwargs) -> StatementProfile:
        """解析银行流水"""
        logging.info(f"解析银行流水: {statement_path}")
        try:
            profiles = []  # 使用列表存储是为了校验该银行流水是否唯一对应格式
            for profile_class in StatementProfile.__subclasses__():
                tag_row = cls.__get_tag_row(statement_path, profile_class.get_check_tags())
                if not tag_row:  # 能获取到标签行，就说明能匹配这一类银行
                    continue
                profiles.append(profile_class(statement_path=statement_path, tag_row=tag_row, **kwargs))
            if not len(profiles):
                raise ValueError(f"银行流水无法识别: {statement_path}")
            elif len(profiles) > 1:
                raise ValueError("银行流水匹配多种格式: %s" % "、".join([each.bank_name for each in profiles]))
            else:
                statement_profile = profiles[0]
                logging.info(f"银行流水的类型为: {statement_profile.bank_name}")
                statement_profile.parse_statement()  # 调用解析流水方法
                return statement_profile
        except xlrd.XLRDError:
            # 因为财务公司的银行流水本质上是html，无法使用xlrd读取，因此当报错XLRDError时，就说明流水银行类型为财务公司
            logging.warning("银行流水的类型为html类型的财务公司，转换后重新处理")
            temp_statement_path = FileUtil.get_temp_path(os.path.basename(statement_path))
            return cls.parse_statement(ExcelUtil.xls_to_xlsx(statement_path, temp_statement_path), **kwargs)

    @staticmethod
    def __get_tag_row(statement_path: str, check_tags: typing.List[str]) -> int:
        """获取表头所在行"""
        workbook = xlrd.open_workbook(statement_path)
        worksheet = workbook.sheet_by_name(workbook.sheet_names()[0])
        for row in range(min(worksheet.nrows, 50)):
            row_values = [str(each).strip() for each in worksheet.row_values(row)]
            if set(check_tags) <= set(row_values):
                return row
