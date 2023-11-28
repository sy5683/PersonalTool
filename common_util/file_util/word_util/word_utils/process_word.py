from docx import shared
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run


class ProcessWord:
    """处理word"""

    @classmethod
    def set_run(cls, run: Run, bold: bool, font_size: int, font_type: str):
        """
        设置run参数
        :param run:
        :param bold: 默认不加粗
        :param font_size: 默认四号字体
        :param font_type: 默认宋体
        :return:
        """
        # 设置字体加粗
        run.bold = bold
        # 设置字体大小
        run.font.size = shared.Pt(font_size)  # 四号字体
        # 设置字体类型
        run.font.name = font_type  # 这个方法只会设置英文和数字
        run.font._element.rPr.rFonts.set(qn('w:eastAsia'), font_type)  # 这个方法只会设置中文

    @staticmethod
    def set_paragraph_alignment(paragraph: Paragraph, alignment: WD_PARAGRAPH_ALIGNMENT):
        """设置段落居中"""
        paragraph.paragraph_format.alignment = alignment

    @staticmethod
    def set_paragraph_indent(paragraph: Paragraph, indent_size: int):
        """设置段落开头缩进"""
        paragraph.paragraph_format.first_line_indent = shared.Pt(indent_size)

    @staticmethod
    def set_paragraph_left_indent(paragraph: Paragraph, indent_size: int):
        """设置段落左侧缩进"""
        paragraph.paragraph_format.left_indent = 0  # 预先对缩进赋值，防止对象为空报错
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:firstLineChars"), str(indent_size))
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:firstLine"), str(indent_size))
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:leftChars"), str(indent_size))
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:left"), str(indent_size))

    @staticmethod
    def set_paragraph_space_after(paragraph: Paragraph, indent_size: int):
        """设置段落结尾行距"""
        paragraph.paragraph_format.space_after = shared.Pt(indent_size)

    @staticmethod
    def set_paragraph_space_before(paragraph: Paragraph, indent_size: int):
        """设置段落开始行距"""
        paragraph.paragraph_format.space_before = shared.Pt(indent_size)
