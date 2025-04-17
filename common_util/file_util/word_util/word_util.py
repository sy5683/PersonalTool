import typing

from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from docx.text.run import Run

from .word_utils.convert_word.convert_word import ConvertWord
from .word_utils.process_word import ProcessWord
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
    def set_run(run: Run, bold: bool = False, font_size: int = 14, font_type: str = '宋体'):
        """设置run参数"""
        ProcessWord.set_run(run, bold=bold, font_size=font_size, font_type=font_type)

    @staticmethod
    def set_paragraph_alignment(paragraph: Paragraph, alignment: WD_PARAGRAPH_ALIGNMENT):
        """设置段落居中"""
        ProcessWord.set_paragraph_alignment(paragraph, alignment)

    @staticmethod
    def set_paragraph_indent(paragraph: Paragraph, indent_size: int):
        """设置段落开头缩进"""
        ProcessWord.set_paragraph_indent(paragraph, indent_size)

    @staticmethod
    def set_paragraph_left_indent(paragraph: Paragraph, indent_size: int = 0):
        """设置段落左侧缩进"""
        ProcessWord.set_paragraph_left_indent(paragraph, indent_size)

    @staticmethod
    def set_paragraph_space_after(paragraph: Paragraph, indent_size: int):
        """设置段落结尾行距"""
        ProcessWord.set_paragraph_space_after(paragraph, indent_size)

    @staticmethod
    def set_paragraph_space_before(paragraph: Paragraph, indent_size: int):
        """设置段落开始行距"""
        ProcessWord.set_paragraph_space_before(paragraph, indent_size)

    @staticmethod
    def word_to_excel(word_path: typing.Union[pathlib.Path, str], save_path: typing.Union[pathlib.Path, str] = None) -> str:
        """word转excel"""
        return ConvertWord.word_to_excel(str(word_path), save_path)

    @staticmethod
    def word_to_pdf(word_path: typing.Union[pathlib.Path, str], save_path: typing.Union[pathlib.Path, str] = None) -> str:
        """word转pdf"""
        return ConvertWord.word_to_pdf(str(word_path), save_path)
