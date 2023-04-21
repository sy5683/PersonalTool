import datetime

from ..base.info_base import InfoBase
from ...util.date_util import DateUtil


class BasicInfo(InfoBase):

    def __init__(self):
        self.name = "解劲松"
        self.birthday = datetime.date(1997, 12, 5)
        self.age = abs(DateUtil.get_year_between_dates(self.birthday, datetime.datetime.now()))

    def to_text(self):
        """转换为文本"""
        return f"|{self.name}|"
