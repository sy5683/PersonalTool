from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.text.paragraph import Paragraph

from personal_tool.local_file.resume_creator.config.resume_word_config import ResumeWordConfig
from personal_tool.local_file.resume_creator.entity.base.info_base import InfoBase
from personal_tool.local_file.resume_creator.util.word_util import WordUtil


class WordFeature:

    @staticmethod
    def add_title(document: Document):
        """添加标题"""
        paragraph = document.add_paragraph()
        run = paragraph.add_run("个人简历")
        WordUtil.set_bold(run)
        WordUtil.set_font_size(run, 26)  # 标题设置为一号字体
        WordUtil.set_font_type(run, ResumeWordConfig.title_font_type)
        WordUtil.set_paragraph_alignment(paragraph, WD_PARAGRAPH_ALIGNMENT.CENTER)

    @classmethod
    def add_info(cls, document: Document):
        """添加信息"""
        # 添加标题
        heading = document.add_heading()
        cls._add_heading(heading, "基本信息")
        # 添加段落
        paragraph = document.add_paragraph()
        for info_class in InfoBase.__subclasses__():
            info = info_class()
            cls._add_body(paragraph, info.to_text())

    @staticmethod
    def _add_heading(heading: Paragraph, context: str):
        run = heading.add_run(context)
        WordUtil.set_font_size(run, ResumeWordConfig.title_font_size)
        WordUtil.set_font_type(run, ResumeWordConfig.title_font_type)

    @staticmethod
    def _add_body(paragraph: Paragraph, context: str):
        run = paragraph.add_run(f"\t{context}\n")
        WordUtil.set_font_size(run, ResumeWordConfig.body_font_size)
        WordUtil.set_font_type(run, ResumeWordConfig.body_font_type)
