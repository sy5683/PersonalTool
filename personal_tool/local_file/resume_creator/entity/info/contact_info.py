from typing import List

from personal_tool.local_file.resume_creator.entity.base.info_base import InfoBase


class ContactInfo(InfoBase):

    def __init__(self):
        super().__init__("联系方式")
        self.phone = "13677365683"
        self.qq = "1079272233"
        self.email_address = f"{self.qq}@qq.com"

    def to_contexts(self) -> List[str]:
        """转换为文本"""
        return [f"{self.phone} | {self.email_address}"]
