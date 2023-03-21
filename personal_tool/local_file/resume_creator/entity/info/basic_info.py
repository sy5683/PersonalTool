import datetime

from personal_tool.local_file.resume_creator.feature.date_feature import DateFeature


class BasicInfo:

    def __init__(self):
        self.name = "解劲松"
        self.birthday = datetime.date(1997, 12, 5)
        self.age = self._get_age()

    def _get_age(self):
        return abs(DateFeature.get_year_between_dates(self.birthday, datetime.datetime.now()))
