import typing
from pathlib import Path

from docx.table import _Cell
from docx.text.paragraph import Paragraph

from .word_utils.convert_word import ConvertWord
from .word_utils.replace_word import ReplaceDocx


class WordUtil:

    @staticmethod
    def replace_paragraph(paragraph: Paragraph, replace_from: str, replace_to: str):
        """替换段落内容"""
        ReplaceDocx.replace_paragraph(paragraph, replace_from, replace_to)

    @staticmethod
    def replace_tabel_cell(cell: _Cell, replace_from: str, replace_to: str):
        """替换表格单元格内容"""
        ReplaceDocx.replace_tabel_cell(cell, replace_from, replace_to)

    @staticmethod
    def word_to_excel(word_path: typing.Union[Path, str]) -> str:
        """word转excel"""
        return ConvertWord.word_to_excel(str(word_path))
