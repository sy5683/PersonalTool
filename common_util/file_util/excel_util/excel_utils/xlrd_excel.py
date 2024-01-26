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
        workbook = xlrd.open_workbook(excel_path, formatting_info=True)
        worksheet = workbook.sheet_by_name(sheet_name) if sheet_name else workbook.sheet_by_index(sheet_index)
        data_list = []
        # 获取表头
        tags = cls._get_tags(worksheet, tag_row, tag_row_quantity)
        for row in range(tag_row + tag_row_quantity, worksheet.nrows):
            keys = [f"{tag}_{index}" if tags.count(tag) > 1 else tag for index, tag in enumerate(tags)]
            row_values = cls.__get_row_values(worksheet, row)
            if not row_values:
                continue  # 去除全空的行
            data = dict(zip(keys, row_values))
            data.update({'_row': row})
            data_list.append(data)
        return data_list

    @classmethod
    def _get_tags(cls, worksheet: xlrd.sheet.Sheet, tag_row: int, tag_row_quantity: int):
        """获取表头，如果有多行表头时，自动将相同列的表头数据合并"""
        tags_map = []
        for row in [(tag_row + index) for index in range(tag_row_quantity)]:
            # 获取表头
            tags = cls.__get_row_values(worksheet, row)
            # 将横向合并单元格的空单元格中赋值合并单元格的值
            for col, tag in enumerate(tags):
                # 无法处理第一列单元
                if not col:
                    continue
                if tag:
                    continue
                merged_coordinate = cls.__get_merged_coordinate(worksheet, row, col)
                # 赋值合并的单元格值
                if merged_coordinate:
                    from_row, to_row, from_col, to_col = merged_coordinate
                    # 纵向合并的表头不在这处理，如果这里不跳过，则会导致合并出错误的表头
                    if to_col - from_col <= 1:
                        continue
                else:
                    # 如果当前单元格下方的单元格有值，则表头需要取合并值
                    for child_row in [(tag_row + index) for index in range(tag_row_quantity)]:
                        if child_row <= row:
                            continue
                        if worksheet.cell(child_row, col).value:
                            break
                    else:
                        continue
                tags[col] = tags[col - 1]
            tags_map.append(tags)
        # 组合单元格表头
        excel_tags = copy.deepcopy(tags_map[0])
        for map_index, tags in enumerate(tags_map[1:]):
            for tag_index, tag in enumerate(tags):
                excel_tags[tag_index] += tag
        return excel_tags

    @staticmethod
    def __get_merged_coordinate(worksheet: xlrd.sheet.Sheet, row: int, col) -> typing.Tuple[int, int, int, int]:
        """获取单元格所在的合并单元格坐标"""
        for from_row, to_row, from_col, to_col in worksheet.merged_cells:
            if from_row <= row < to_row and from_col <= col < to_col:
                return from_row, to_row, from_col, to_col

    @staticmethod
    def __get_row_values(worksheet: xlrd.sheet.Sheet, row: int) -> typing.List[str]:
        """获取行数据"""
        row_values = []
        for col, value in enumerate(worksheet.row_values(row)):
            # 字符串化数据并去除异常字符与空字符
            value = str(value).replace("\x00", "").strip()
            # 某些特殊的单元格需要特殊处理
            cell = worksheet.cell(row, col)
            if cell.ctype == 2:  # 数字类型，需要去除掉excel数据中数字字符串中".0"结尾的小数
                value = FormatExcelData.format_int_data(value)
            if cell.ctype == 3:  # 日期类型，需要将excel中的日期数据转换为标准日期字符串
                value = FormatExcelData.format_date_data(value, "%Y-%m-%d")
            row_values.append(value)
        return row_values
