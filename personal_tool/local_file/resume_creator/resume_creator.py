import os.path
import tempfile

import docx
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from base.tool_base import ToolBase
from config.resume_word_config import ResumeWordConfig
from personal_tool.local_file.resume_creator.entity.info.basic_info import BasicInfo
from util.win32_util import Win32Util
from util.word_util import WordUtil


class ResumeCreator(ToolBase):
    """简历生成器"""

    def __init__(self):
        self.save_path = tempfile.mkdtemp()
        self.resume_path = os.path.join(self.save_path, "个人简历.docx")
        self.document = docx.Document()

    def main(self):
        self._add_title()

        self.document.save(self.resume_path)
        # Win32Util.open_file(self.save_path)
        Win32Util.open_file(self.resume_path)

    def _add_title(self):
        """添加标题"""
        paragraph = self.document.add_paragraph()
        basic_info = BasicInfo()
        run = paragraph.add_run(basic_info.to_text())
        WordUtil.set_bold(run)
        WordUtil.set_font_size(run, 26)  # 标题设置为一号字体
        WordUtil.set_font_type(run, ResumeWordConfig.title_font_type)
        WordUtil.set_paragraph_alignment(paragraph, WD_PARAGRAPH_ALIGNMENT.CENTER)


if __name__ == '__main__':
    resume_creator = ResumeCreator()
    resume_creator.main()
