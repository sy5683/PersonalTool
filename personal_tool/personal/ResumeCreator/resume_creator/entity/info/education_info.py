import typing

from ..base.info_base import InfoBase


class EducationInfo(InfoBase):

    def __init__(self):
        super().__init__("教育背景")
        self.school_name = "湖南理工学院"  # 毕业学校
        self.qualification = "本科"  # 学历
        self.from_date = "2015年09月"  # 入学时间
        self.to_date = "2019年06月"  # 毕业时间
        self.major = "软件工程"  # 专业

    def to_contexts(self) -> typing.List[str]:
        """转换为文本"""
        return [f"{self.school_name} | {self.from_date}-{self.to_date}", f"专业: {self.major}"]
