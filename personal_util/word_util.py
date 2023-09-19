import copy
import logging
from typing import Tuple

from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.shared import RGBColor
from docx.table import _Cell
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

    @staticmethod
    def set_paragraph_space_after(paragraph: Paragraph, indent_size: int):
        """设置段落结尾行距"""
        paragraph.paragraph_format.space_after = Pt(indent_size)

    @staticmethod
    def set_paragraph_space_before(paragraph: Paragraph, indent_size: int):
        """设置段落开始行距"""
        paragraph.paragraph_format.space_before = Pt(indent_size)

    @classmethod
    def replace_paragraph(cls, paragraph: Paragraph, replace_from: str, replace_to: str):
        """替换段落内容"""
        try:
            template_paragraph = copy.deepcopy(paragraph)
            paragraph.text = paragraph.text.replace(replace_from, replace_to)
            cls._copy_paragraph_format(paragraph, template_paragraph)  # 复制段落格式
        except TypeError:
            logging.warning(f"段落值【{replace_from}】替换失败: {replace_to}")

    @classmethod
    def replace_tabel_cell(cls, cell: _Cell, replace_from: str, replace_to: str):
        """替换表格单元格内容"""
        try:
            template_paragraphs = copy.deepcopy(cell.paragraphs)  # 保存原始段落的run，用于保留格式
            cell.text = cell.text.replace(replace_from, replace_to)
            for index, paragraph in enumerate(cell.paragraphs):
                template_paragraph = template_paragraphs[index]
                cls.set_left_indent(paragraph)
                cls._copy_paragraph_format(paragraph, template_paragraph)  # 复制段落格式
        except TypeError:
            logging.warning(f"表格值【{replace_from}】替换失败: {replace_to}")

    @staticmethod
    def set_left_indent(paragraph: Paragraph, indent_size: int = 0):
        """设置左侧缩进"""
        paragraph.paragraph_format.left_indent = 0  # 预先对缩进赋值，防止对象为空报错
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:firstLineChars"), str(indent_size))
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:firstLine"), str(indent_size))
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:leftChars"), str(indent_size))
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:left"), str(indent_size))

    @staticmethod
    def _copy_paragraph_format(paragraph: Paragraph, template_paragraph: Paragraph):
        """复制段落格式"""
        paragraph.paragraph_format.alignment = template_paragraph.paragraph_format.alignment
        paragraph.paragraph_format.line_spacing = template_paragraph.paragraph_format.line_spacing
        for index, run in enumerate(paragraph.runs):
            run.bold = template_paragraph.runs[index].bold
            run.font.color.rgb = template_paragraph.runs[index].font.color.rgb
            run.font.name = template_paragraph.runs[index].font.name
            # .font.name只能设置英文和数字，中文无法取值暂时搁置
            run.font.size = template_paragraph.runs[index].font.size
            run.italic = template_paragraph.runs[index].italic
            run.style = template_paragraph.runs[index].style
            run.style.name = template_paragraph.runs[index].style.name
            run.underline = template_paragraph.runs[index].underline
