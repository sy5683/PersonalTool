import datetime
import typing

from common_util.data_util.time_util.time_util import TimeUtil
from ..base.info_base import InfoBase


class BasicInfo(InfoBase):

    def __init__(self):
        super().__init__("基本信息")
        self.name = "解劲松"  # 姓名
        self.birthday = datetime.date(1997, 12, 5)  # 生日
        self.age = TimeUtil.get_years_between_dates(self.birthday, datetime.datetime.now())  # 年龄

    def to_contexts(self) -> typing.List[str]:
        """转换为文本"""
        return [f"姓名: {self.name}\t年龄: {self.age}岁"]
