import logging
import os
import typing
from pathlib import Path

import docx
import openpyxl


class ConvertWord:
    """转换word"""

    @staticmethod
    def word_to_excel(word_path: str, save_path: typing.Union[Path, str]) -> str:
        """word转excel"""
        logging.info(f"开始将Word文件转换为Excel: {word_path}")
        document = docx.Document(word_path)
        workbook = openpyxl.Workbook()
        for index, table in enumerate(document.tables):
            worksheet = workbook.active if not index else workbook.create_sheet()
            for row_index, row in enumerate(table.rows):
                for col_index, cell in enumerate(row.cells):
                    worksheet.cell(row_index + 1, col_index + 1, cell.text)
        save_path = f"{os.path.splitext(word_path)[0]}.xlsx" if save_path is None else str(save_path)
        workbook.save(save_path)
        workbook.close()
        logging.info(f"成功将Word文件转换为Excel: {save_path}")
        return save_path
