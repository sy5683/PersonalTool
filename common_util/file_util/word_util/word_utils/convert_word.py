import os.path

import docx
import openpyxl


class ConvertWord:
    """转换word"""

    @staticmethod
    def word_to_excel(word_path: str) -> str:
        """word转excel"""
        document = docx.Document(word_path)
        workbook = openpyxl.Workbook()
        for index, table in enumerate(document.tables):
            worksheet = workbook.active if not index else workbook.create_sheet()
            for row_index, row in enumerate(table.rows):
                for col_index, cell in enumerate(row.cells):
                    worksheet.cell(row_index + 1, col_index + 1, cell.text)
        excel_path = f"{os.path.splitext(word_path)[0]}.xlsx"
        workbook.save(excel_path)
        workbook.close()
        return excel_path
