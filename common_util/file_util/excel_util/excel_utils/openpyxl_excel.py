import re
import typing

from openpyxl import utils
from openpyxl.worksheet.worksheet import Worksheet


class OpenpyxlExcel:

    @staticmethod
    def merge_cells(worksheet: Worksheet, coordinate_from: str, coordinate_to: str):
        """合并单元格"""
        # 处理起始坐标与结束坐标，使起始坐标必须在结束坐标左上
        from_col, from_row = [each for each in re.compile(r'(\d+|\s+)').split(coordinate_from) if each]
        to_col, to_row = [each for each in re.compile(r'(\d+|\s+)').split(coordinate_to) if each]
        new_from_col, new_to_col = (from_col, to_col) if from_col < to_col else (to_col, from_col)
        new_from_row, new_to_row = (from_row, to_row) if int(from_row) < int(to_row) else (to_row, from_row)
        # 合并单元格
        worksheet.merge_cells(f"{new_from_col}{new_from_row}:{new_to_col}{new_to_row}")

    @staticmethod
    def get_sheet_heights(worksheet: Worksheet) -> typing.List[float]:
        """获取sheet行高"""
        heights = []
        for row in range(worksheet.max_row):
            row_height = worksheet.row_dimensions[row + 1].height
            heights.append(row_height)
        return heights

    @staticmethod
    def get_sheet_widths(worksheet: Worksheet) -> typing.List[float]:
        """获取sheet列宽"""
        widths = []
        for col in range(worksheet.max_column):
            col_letter = utils.get_column_letter(col + 1)
            col_width = worksheet.column_dimensions[col_letter].width
            widths.append(col_width)
        return widths

    @staticmethod
    def set_sheet_heights(worksheet: Worksheet, heights: typing.List[typing.Union[float, None]]):
        """设置sheet行高"""
        for index, height in enumerate(heights):
            if height is None:  # 当设置行高为None时，不修改列值
                continue
            worksheet.row_dimensions[index + 1].height = height

    @staticmethod
    def set_sheet_widths(worksheet: Worksheet, widths: typing.List[typing.Union[float, None]]):
        """设置sheet列宽"""
        for index, width in enumerate(widths):
            if width is None:  # 当设置列宽为None时，不修改列值
                continue
            col_letter = utils.get_column_letter(index + 1)
            worksheet.column_dimensions[col_letter].width = width
