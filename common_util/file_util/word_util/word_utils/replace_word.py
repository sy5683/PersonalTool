import copy
import logging

from docx.table import _Cell
from docx.text.paragraph import Paragraph

from .process_word import ProcessWord


class ReplaceDocx:
    """替换word"""

    @classmethod
    def replace_paragraph(cls, paragraph: Paragraph, replace_from: str, replace_to: str):
        """替换段落内容"""
        try:
            template_paragraph = copy.deepcopy(paragraph)
            paragraph.text = paragraph.text.replace(replace_from, replace_to)
            cls._copy_paragraph_format(paragraph, template_paragraph)
        except TypeError:
            logging.warning(f"段落值【{replace_from}】替换至【{replace_to}】失败: {paragraph.text}")

    @classmethod
    def replace_tabel_cell(cls, cell: _Cell, replace_from: str, replace_to: str):
        """替换表格单元格内容"""
        try:
            template_paragraphs = copy.deepcopy(cell.paragraphs)
            cell.text = cell.text.replace(replace_from, replace_to)
            for index, paragraph in enumerate(cell.paragraphs):
                ProcessWord.set_paragraph_left_indent(paragraph)
                cls._copy_paragraph_format(paragraph, template_paragraphs[index])
        except TypeError:
            logging.warning(f"表格值【{replace_from}】替换至【{replace_to}】失败: {cell.text}")

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
