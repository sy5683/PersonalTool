from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from personal_tool.local_file.resume_creator.config.resume_word_config import ResumeWordConfig
from personal_tool.local_file.resume_creator.entity.base.experience_base import ProjectExperience
from personal_tool.local_file.resume_creator.entity.base.info_base import InfoBase
from personal_tool.local_file.resume_creator.util.word_util import WordUtil


class WordFeature:

    @staticmethod
    def add_title(document: Document):
        """添加标题"""
        paragraph = document.add_paragraph()
        WordUtil.set_paragraph_alignment(paragraph, WD_PARAGRAPH_ALIGNMENT.CENTER)
        run = paragraph.add_run("个人简历")
        WordUtil.set_bold(run)
        WordUtil.set_font_type(run, ResumeWordConfig.title_font_type)
        WordUtil.set_font_size(run, ResumeWordConfig.title_font_size)

    @classmethod
    def add_info(cls, document: Document):
        """添加信息"""
        # 1) 添加标题
        heading = document.add_heading(level=1)
        run = heading.add_run("基本信息")
        WordUtil.set_bold(run)
        WordUtil.set_font_type(run, ResumeWordConfig.heading_font_type)
        WordUtil.set_font_size(run, ResumeWordConfig.heading_font_size_1)
        # 2) 添加段落
        for info_class in InfoBase.__subclasses__():
            info = info_class()
            paragraph = document.add_paragraph()
            WordUtil.set_paragraph_indent(paragraph, 10)
            run = paragraph.add_run(info.to_text())
            WordUtil.set_font_type(run, ResumeWordConfig.body_font_type)
            WordUtil.set_font_size(run, ResumeWordConfig.body_font_size)

    @classmethod
    def add_project_experience(cls, document: Document):
        """添加项目经验"""
        # 1) 添加标题
        heading = document.add_heading(level=1)
        run = heading.add_run("项目经验")
        WordUtil.set_bold(run)
        WordUtil.set_font_type(run, ResumeWordConfig.heading_font_type)
        WordUtil.set_font_size(run, ResumeWordConfig.heading_font_size_1)
        # 2) 添加段落
        for project_experience_class in ProjectExperience.__subclasses__():
            project_experience = project_experience_class()
            heading = document.add_heading(level=2)
            WordUtil.set_paragraph_indent(heading, 10)
            run = heading.add_run(project_experience.get_project_name())
            WordUtil.set_font_type(run, ResumeWordConfig.heading_font_type)
            WordUtil.set_font_size(run, ResumeWordConfig.heading_font_size_2)

    @staticmethod
    def _add_heading(document: Document, content: str):
        heading = document.add_heading(level=1)
        run = heading.add_run(content)
        WordUtil.set_bold(run)
        WordUtil.set_font_type(run, ResumeWordConfig.heading_font_type)
        WordUtil.set_font_size(run, ResumeWordConfig.heading_font_size_1)
