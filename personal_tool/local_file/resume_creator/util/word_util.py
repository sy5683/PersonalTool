from typing import Tuple, Union

import docx
from docx.document import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.shared import RGBColor
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run


class WordUtil:

    @staticmethod
    def set_bold(run: Run):
        """设置字体加粗"""
        run.bold = True

    @staticmethod
    def set_font_color(run: Run, color: Tuple[int, int, int]):
        """设置字体颜色"""
        run.font.color.rgb = RGBColor(color[0], color[1], color[2])

    @staticmethod
    def set_font_size(run: Run, font_size: int):
        """设置字体大小"""
        run.font.size = Pt(font_size)  # 设置字体时必须要使用Pt方法对其处理为预设的字体

    @staticmethod
    def set_font_type(run: Run, font_type: str):
        """设置字体类型"""
        run.font.name = font_type  # 这个方法只会设置英文和数字
        run.font._element.rPr.rFonts.set(qn('w:eastAsia'), font_type)  # 这个方法只会设置中文

    @staticmethod
    def set_paragraph_alignment(paragraph: Paragraph, alignment: WD_PARAGRAPH_ALIGNMENT):
        """设置段落居中"""
        paragraph.paragraph_format.alignment = alignment

    @staticmethod
    def set_paragraph_indent(paragraph: Paragraph, indent_size: int):
        """设置段落开头缩进"""
        paragraph.paragraph_format.first_line_indent = Pt(indent_size)
