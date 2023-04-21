from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from personal_tool.local_file.resume_creator.config.resume_word_config import ResumeWordConfig
from personal_tool.local_file.resume_creator.entity.info.basic_info import BasicInfo
from personal_tool.local_file.resume_creator.entity.info.contact_info import ContactInfo
from personal_tool.local_file.resume_creator.util.word_util import WordUtil


class WordFeature:

    @staticmethod
    def add_title(document: Document):
        """添加标题（基本信息）"""
        paragraph = document.add_paragraph()
        basic_info = BasicInfo()
        run = paragraph.add_run(basic_info.name)
        WordUtil.set_bold(run)
        WordUtil.set_font_size(run, 26)  # 标题设置为一号字体
        WordUtil.set_font_type(run, ResumeWordConfig.title_font_type)
        WordUtil.set_paragraph_alignment(paragraph, WD_PARAGRAPH_ALIGNMENT.CENTER)

    @staticmethod
    def add_contact_info(document: Document):
        """添加联系信息"""
        paragraph = document.add_paragraph()
        contact_info = ContactInfo()
        run = paragraph.add_run(f"{contact_info.phone}\n{contact_info.email_address}")
        WordUtil.set_font_type(run, ResumeWordConfig.body_font_type)
