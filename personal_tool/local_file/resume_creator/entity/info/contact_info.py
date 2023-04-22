from personal_tool.local_file.resume_creator.entity.base.info_base import InfoBase


class ContactInfo(InfoBase):

    def __init__(self):
        super().__init__("联系方式")
        self.phone = "13677365683"
        self.email_address = "1079272233@qq.com"

    def to_text(self) -> str:
        """转换为文本"""
        return f"联系方式: {self.phone}|{self.email_address}"
