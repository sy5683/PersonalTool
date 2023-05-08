from typing import List

from personal_tool.local_file.resume_creator.entity.base.info_base import InfoBase


class PersonalInfo(InfoBase):

    def __init__(self):
        super().__init__("个人信息")
        self.skills = []
        self.profile = ""

    def to_contexts(self) -> List[str]:
        """转换为文本"""
        return [""]
