import typing
from pathlib import Path

from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from .excel_utils.process_excel.convert_excel.convert_excel import ConvertExcel
from .excel_utils.process_excel.copy_xlsx import CopyXlsx
from .excel_utils.process_excel.openpyxl_excel import OpenpyxlExcel
from .excel_utils.process_excel_data.format_excel_data import FormatExcelData
from .excel_utils.process_excel_data.verify_excel_data import VerifyExcelData
from .excel_utils.read_excel import ParseExcel


class ExcelUtil:

    @staticmethod
    def add_title(worksheet: Worksheet, title: str, length: int, title_size: float = 20):
        """添加标题"""
        OpenpyxlExcel.add_title(worksheet, title, length, title_size)

    @staticmethod
    def add_tag(worksheet: Worksheet, tags: typing.List[str], tag_row: int, tag_size: float = 14,
                tag_color: str = '9BC2E6'):
        """添加表头"""
        OpenpyxlExcel.add_tag(worksheet, tags, tag_row, tag_size, tag_color)

    @staticmethod
    def copy_sheet(worksheet: Worksheet, copy_worksheet: Worksheet):
        """复制excel的sheet并带上相应格式"""
        CopyXlsx.copy_sheet(worksheet, copy_worksheet)

    @staticmethod
    def excel_to_images(file_path: typing.Union[Path, str],
                        save_path: typing.Union[Path, str] = None) -> typing.List[str]:
        """excel转图片"""
        return ConvertExcel.excel_to_images(str(file_path), save_path)

    @staticmethod
    def format_data(data: any):
        """处理数据"""
        return FormatExcelData.format_data(data)

    @staticmethod
    def format_date_data(date: typing.Union[float, str]) -> str:
        """格式化日期数据"""
        return FormatExcelData.format_date_data(date)

    @staticmethod
    def format_int_data(data: typing.Union[float, str]) -> str:
        """格式化整数数据"""
        return FormatExcelData.format_int_data(str(data))

    @staticmethod
    def get_data_list(excel_path: typing.Union[Path, str], sheet_index: int = 0, sheet_name: str = None,
                      tag_row: int = 0, tag_row_quantity: int = 1) -> typing.List[dict]:
        """获取excel数据"""
        return ParseExcel.get_data_list(str(excel_path), sheet_index, sheet_name, tag_row, tag_row_quantity)

    @staticmethod
    def re_save_excel(excel_path: typing.Union[Path, str]):
        """重新保存excel"""
        ConvertExcel.re_save_excel(str(excel_path))

    @staticmethod
    def set_cell(cell: Cell, value: any = '_no_value', number_format: str = None,
                 horizontal: typing.Optional[str] = '_no_horizontal', vertical: typing.Optional[str] = '_no_vertical',
                 fill_color: typing.Optional[str] = '_no_fill_color', is_border: bool = None,
                 font_size: float = None, is_bold: bool = None, is_italic: bool = None,
                 font_color: typing.Optional[str] = '_no_font_color'
                 ):
        """设置单元格"""
        OpenpyxlExcel.set_cell(cell, value, number_format, horizontal, vertical, fill_color, is_border, font_size,
                               is_bold, is_italic, font_color)

    @staticmethod
    def set_cell_money_format(cell: Cell):
        """设置金额单元格"""
        OpenpyxlExcel.set_cell(cell, number_format=r'_ * #,##0.00_ ;_ * \-#,##0.00_ ;_ * "-"??_ ;_ @_ ',
                               horizontal='right')

    @staticmethod
    def set_cell_percentage_format(cell: Cell):
        """设置百分数单元格"""
        OpenpyxlExcel.set_cell(cell, number_format='0.00%', horizontal='center')

    @staticmethod
    def set_sheet_widths(worksheet: Worksheet, widths: typing.List[typing.Union[float, None]]):
        """设置sheet列宽"""
        OpenpyxlExcel.set_sheet_widths(worksheet, widths)

    @staticmethod
    def verify_scientific_notation(value: str):
        """校验科学计数法"""
        VerifyExcelData.verify_scientific_notation(value)

    @staticmethod
    def xls_to_xlsx(excel_path: typing.Union[Path, str], save_path: typing.Union[Path, str] = None) -> str:
        """xls文件转换为xlsx文件"""
        return ConvertExcel.xls_to_xlsx(str(excel_path), save_path)
