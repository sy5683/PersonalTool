import datetime

from personal_tool.local_file.resume_creator.util.date_util import DateUtil


class BasicInfo:

    def __init__(self):
        self.name = "解劲松"
        self.birthday = datetime.date(1997, 12, 5)
        self.age = abs(DateUtil.get_year_between_dates(self.birthday, datetime.datetime.now()))
