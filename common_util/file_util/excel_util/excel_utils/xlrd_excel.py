import copy
import typing

import xlrd

from .format_excel_data import FormatExcelData


class XlrdExcel:

    @classmethod
    def get_data_list(cls, excel_path: str, sheet_index: int, sheet_name: str, tag_row: int,
                      tag_row_quantity: int) -> typing.List[dict]:
        """
        获取excel数据
        通过1.2.0版本的xlrd可以同时读取xls和xlsx文件
        通过标签行生成字典key，然后标签行以下全部数据添加进字典列表中
        """
        workbook = xlrd.open_workbook(excel_path)
        if sheet_name:
            worksheet = workbook.sheet_by_name(sheet_name)
        else:
            worksheet = workbook.sheet_by_index(sheet_index)
        data_list = []
        tags = cls._get_tags(worksheet, tag_row, tag_row_quantity)
        for row in range(tag_row + tag_row_quantity, worksheet.nrows):
            keys = [f"{tag}_{index}" if tags.count(tag) > 1 else tag for index, tag in enumerate(tags)]
            row_values = cls.__get_row_values(worksheet, row)
            # 去除全空的行
            if not row_values:
                continue
            data = dict(zip(keys, row_values))
            data.update({'_row': row})
            data_list.append(data)
        return data_list

    @classmethod
    def _get_tags(cls, worksheet: xlrd.sheet.Sheet, tag_row: int, tag_row_quantity: int):
        """获取表头，如果有多行表头时，自动将相同列的表头数据合并"""
        tags_map = []
        for index in range(tag_row_quantity):
            tags_map.append(cls.__get_row_values(worksheet, tag_row + index))
        excel_tags = copy.deepcopy(tags_map[0])
        for map_index, tags in enumerate(tags_map[1:]):
            for tag_index, tag in enumerate(tags):
                last_tags = tags_map[map_index]
                if tag and not last_tags[tag_index]:
                    last_tag = ""
                    for temp_index in range(tag_index):
                        last_tag = last_tags[tag_index - temp_index]
                        if last_tag:
                            break
                    tag = last_tag + tag
                excel_tags[tag_index] += tag
        return excel_tags

    @staticmethod
    def __get_row_values(worksheet: xlrd.sheet.Sheet, row: int) -> typing.List[str]:
        row_values = []
        for col, value in enumerate(worksheet.row_values(row)):
            # 字符串化数据并去除异常字符与空字符
            value = str(value).replace("\x00", "").strip()
            cell = worksheet.cell(row, col)
            if cell.ctype == 2:  # 数字类型
                # 去除掉excel数据中数字字符串中".0"结尾的小数
                value = FormatExcelData.format_int_data(value)
            if cell.ctype == 3:  # 日期类型
                # 将excel中的日期数据转换为标准日期字符串
                value = FormatExcelData.format_date_data(value, "%Y-%m-%d")
            row_values.append(value)
        return row_values
