import typing

from ..base.info_base import InfoBase


class ContactInfo(InfoBase):

    def __init__(self):
        super().__init__("联系方式")
        self.phone = "13677365683"  # 电话
        self.qq = "1079272233"  # QQ
        self.we_chat = "SKY568372"  # 微信
        self.email_address = f"{self.qq}@qq.com"  # 电子邮箱

    def to_contexts(self) -> typing.List[str]:
        """转换为文本"""
        return [f"电话: {self.phone}"]
