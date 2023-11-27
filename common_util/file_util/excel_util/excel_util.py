import typing
from pathlib import Path

from openpyxl.worksheet.worksheet import Worksheet

from .excel_utils.copy_xlsx import CopyXlsx
from .excel_utils.format_excel_data import FormatExcelData
from .excel_utils.win32_excel import Win32Excel


class ExcelUtil:

    @staticmethod
    def copy_sheet(worksheet: Worksheet, copy_worksheet: Worksheet):
        """复制excel的sheet并带上相应格式"""
        CopyXlsx.copy_sheet(worksheet, copy_worksheet)

    @classmethod
    def format_date_data(cls, date: typing.Union[int, str], time_format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """格式化日期数据"""
        return FormatExcelData.format_date_data(date, time_format)

    @staticmethod
    def format_int_data(data: typing.Union[float, str]) -> str:
        """格式化整数数据"""
        return FormatExcelData.format_int_data(str(data))

    @staticmethod
    def re_save_excel(excel_path: typing.Union[Path, str]):
        """重新保存excel"""
        Win32Excel.re_save_excel(str(excel_path))

    @staticmethod
    def xls_to_xlsx(excel_path: typing.Union[Path, str]) -> str:
        """xls文件转换为xlsx文件"""
        return Win32Excel.xls_to_xlsx(str(excel_path))
