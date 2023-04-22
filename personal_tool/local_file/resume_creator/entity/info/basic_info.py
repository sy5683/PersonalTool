import datetime

from personal_tool.local_file.resume_creator.entity.base.info_base import InfoBase
from personal_tool.local_file.resume_creator.util.date_util import DateUtil


class BasicInfo(InfoBase):

    def __init__(self):
        super().__init__("基本信息")
        self.name = "解劲松"
        self.birthday = datetime.date(1997, 12, 5)
        self.age = abs(DateUtil.get_year_between_dates(self.birthday, datetime.datetime.now()))

    def to_text(self) -> str:
        """转换为文本"""
        return f"姓名: {self.name}\t年龄: {self.age}岁"
