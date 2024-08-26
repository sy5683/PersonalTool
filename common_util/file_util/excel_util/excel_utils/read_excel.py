import typing

import xlrd

from .process_excel_data.format_excel_data import FormatExcelData


class ParseExcel:

    @classmethod
    def get_data_list(cls, excel_path: str, sheet_index: int, sheet_name: str, tag_row: int,
                      tag_row_quantity: int) -> typing.List[dict]:
        """
        获取excel数据
        通过1.2.0版本的xlrd可以同时读取xls和xlsx文件
        通过标签行生成字典key，然后标签行以下全部数据添加进字典列表中
        """
        workbook = xlrd.open_workbook(excel_path)
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
        tag_rows = [(tag_row + index) for index in range(tag_row_quantity)]
        # 将表头以map格式保存，用于后续处理
        row_tags_map = [cls.__get_row_values(worksheet, row) for row in tag_rows]
        # 以列为单位读取表头map，用于父级判断
        tags = []
        for col in range(worksheet.ncols):
            if col:  # 第一列表头不处理，直接合并
                last_col_tags = [row_tags[col - 1] for row_tags in row_tags_map]
                for index, col_tag in enumerate([row_tags[col] for row_tags in row_tags_map]):
                    if not col_tag:
                        last_col_tag = last_col_tags[index]
                        if last_col_tag:
                            row_tags_map[index][col] = last_col_tag  # 直接更新表头map，刷新数据
                    else:  # 如果某一列的表头为正常情况，那么这一列之后的表头都不再处理
                        break
            # 重新从表头map中取数，确保数据唯一，多的数据依次往后添加编号
            add_num = 0
            tag = _temp_tag = "".join([row_tags[col] for row_tags in row_tags_map])
            while tag in tags:
                add_num += 1
                tag = f"{_temp_tag}_{add_num}"
            tags.append(tag)
        return tags

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
                value = FormatExcelData.format_date_data(value)
            row_values.append(value)
        return row_values
