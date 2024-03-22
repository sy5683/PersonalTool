import abc
import logging
import os.path
import re
import traceback
import typing

import xlrd

from common_util.data_util.time_util.time_util import TimeUtil
from .statement import Statement


class StatementParser(metaclass=abc.ABCMeta):

    def __init__(self, bank_name: str, statement_path: str, check_tags: typing.List[str], **kwargs):
        self.bank_name = bank_name  # 银行名称
        self.company_name = kwargs.get("company_name")  # 特殊情况需要使用到公司名称
        self.statement_path = statement_path  # 流水路径
        self.statement_name = os.path.basename(statement_path)
        self.tag_row = self.__get_tag_row(check_tags)  # 表头行
        self.account_number = None  # 银行账号
        self.statements: typing.List[Statement] = []  # 流水数据

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return True if self.tag_row else False

    @abc.abstractmethod
    def parse_statement(self):
        """解析流水"""

    @staticmethod
    def _format_date(date_str: str) -> str:
        """格式化交易时间"""
        return TimeUtil.format_to_str(date_str, time_format="%Y{Y}%m{m}%d{d}%H{H}%M{M}%S{S}")

    def _get_abc_account_info(self) -> typing.Tuple[str, str]:
        """获取农行开户账号信息（开户名称与开户账号）"""
        return "", ""  # TODO

    def _get_special_data(self, *check_tags: str, relative_col: int = 1) -> str:
        """
        获取在表头上方的特殊数据（一般为特殊银行的开户名称或者开户账号）
        获取方式一般为在指定标签单元格的右边一格获取公司名称，因此relative_col默认为1
        """
        special_data_list = []
        workbook = xlrd.open_workbook(self.statement_path)
        worksheet = workbook.sheet_by_name(workbook.sheet_names()[0])
        for row in range(self.tag_row):
            row_values = worksheet.row_values(row)
            for index, value in enumerate(row_values):
                check_tags_str = "|".join(check_tags)
                check_tags_str = check_tags_str.replace("[", r"\[").replace("]", r"\]")
                if re.search(check_tags_str, str(value)):
                    try:
                        special_data_list.append(row_values[index + relative_col])
                    except IndexError:
                        logging.error(traceback.format_exc())
        if not len(special_data_list):
            raise ValueError("无法匹配到指定列: %s" % "、".join(check_tags))
        elif len(special_data_list) > 1:
            raise ValueError("有多行匹配上的列: %s" % "、".join(check_tags))
        else:
            return special_data_list[0].strip()

    def __get_tag_row(self, check_tags: typing.List[str]) -> int:
        """获取表头所在行"""
        workbook = xlrd.open_workbook(self.statement_path)
        worksheet = workbook.sheet_by_name(workbook.sheet_names()[0])
        for row in range(min(worksheet.nrows, 50)):
            row_values = [str(each).strip() for each in worksheet.row_values(row)]
            if set(check_tags) <= set(row_values):
                return row
