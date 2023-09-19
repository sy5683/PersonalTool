from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.text.paragraph import Paragraph
from docx.text.run import Run


class WordUtil:

    @staticmethod
    def set_bold(run: Run):
        """设置字体加粗"""
        run.bold = True

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
