import os.path
import tempfile
from pathlib import Path

import docx

from base.tool_base import ToolBase
from feature.word_feature import WordFeature
from personal_tool.local_file.resume_creator.util.import_util import ImportUtil
from util.win32_util import Win32Util


class ResumeCreator(ToolBase):
    """简历生成器"""

    def __init__(self):
        self.save_path = tempfile.mkdtemp()
        self.resume_path = os.path.join(self.save_path, "个人简历.docx")
        self.document = docx.Document()
        ImportUtil.import_module(Path(__file__).parent.joinpath("entity"))

    def main(self):
        # 1) 添加标题
        WordFeature.add_title(self.document)
        # 2) 添加信息
        WordFeature.add_info(self.document)
        # 3) 添加项目经验
        WordFeature.add_project_experience(self.document)

        self.document.save(self.resume_path)
        # Win32Util.open_file(self.save_path)
        Win32Util.open_file(self.resume_path)


if __name__ == '__main__':
    resume_creator = ResumeCreator()
    resume_creator.main()
