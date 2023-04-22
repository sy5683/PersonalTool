from personal_tool.local_file.resume_creator.entity.base.info_base import InfoBase


class EducationInfo(InfoBase):

    def __init__(self):
        super().__init__("教育背景")
        self.school_name = "湖南理工学院"
        self.qualification = "本科"
        self.from_date = "2015.09"
        self.to_date = "2019.06"
        self.major = "软件工程"

    def to_text(self) -> str:
        """转换为文本"""
        return f"教育背景: {self.school_name}({self.from_date}-{self.to_date})\n\t\t{self.major}专业"
