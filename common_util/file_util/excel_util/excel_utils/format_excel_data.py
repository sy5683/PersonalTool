import re
import typing

import xlrd


class FormatExcelData:

    @staticmethod
    def format_int_data(data: str) -> str:
        """去除掉excel数据中数字字符串读取出来的小数点"""
        return re.sub(r"\.0+$", "", data)

    @classmethod
    def format_date_data(cls, date: typing.Union[int, str], time_format: str) -> str:
        """
        excel中保存日期的时候，可能会有很多种保存方式
        其中最为特殊的一种方式是数字保存
        然后通过计算，将一串数字显示为目标日期
        因此在取的时候，需要对其进行转换
        """
        if isinstance(date, int):
            date = cls._format_excel_date_number(date, time_format)
        elif isinstance(date, str):
            date = cls.format_int_data(date)
            if date.isdigit():
                date = cls._format_excel_date_number(int(date), time_format)
        return date

    @staticmethod
    def _format_excel_date_number(date_number: int, time_format: str) -> str:
        """
        excel中保存日期的时候，可能会有很多种保存方式
        其中最为特殊的一种方式是数字保存
        然后通过计算，将一串数字显示为目标日期
        因此在取的时候，需要对其进行转换
        """
        stamp = xlrd.xldate_as_datetime(date_number, 0)
        return stamp.strftime(time_format).format(Y="年", m="月", d="日", H="时", M="分", S="秒")
