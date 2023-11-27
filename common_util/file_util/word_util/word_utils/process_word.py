from docx.oxml.ns import qn

from docx.text.paragraph import Paragraph


class ProcessWord:
    """处理word"""

    @staticmethod
    def set_paragraph_left_indent(paragraph: Paragraph, indent_size: int = 0):
        """设置段落左侧缩进"""
        paragraph.paragraph_format.left_indent = 0  # 预先对缩进赋值，防止对象为空报错
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:firstLineChars"), str(indent_size))
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:firstLine"), str(indent_size))
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:leftChars"), str(indent_size))
        paragraph.paragraph_format.element.pPr.ind.set(qn("w:left"), str(indent_size))
