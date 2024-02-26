import logging
import os
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
        statement_name = os.path.basename(statement_path)
        try:
            profiles = []
            for profile_class in StatementProfile.__subclasses__():
                profile = profile_class(statement_path=statement_path, **kwargs)
                if profile.judge():
                    profiles.append(profile)
            if not len(profiles):
                raise ValueError(f"银行流水【{statement_name}】无法识别")
            elif len(profiles) > 1:
                raise ValueError(
                    f"银行流水【{statement_name}】匹配多种格式: %s" % "、".join([each.bank_name for each in profiles]))
            else:
                statement_profile = profiles[0]
                logging.info(f"银行流水【{statement_name}】的类型为: {statement_profile.bank_name}流水")
                statement_profile.parse_statement()  # 调用解析流水方法
                return statement_profile
        except xlrd.XLRDError:
            # 因为财务公司的银行流水本质上是html，无法使用xlrd读取，因此当报错XLRDError时，就说明流水银行类型为财务公司
            logging.warning(f"银行流水【{statement_name}】的类型为html类型的财务公司，转换后重新处理")
            new_statement_path = ExcelUtil.xls_to_xlsx(statement_path, FileUtil.get_temp_path(statement_name))
            return cls.parse_statement(new_statement_path, **kwargs)
