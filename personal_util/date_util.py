import datetime
from typing import Union

from dateutil.relativedelta import relativedelta


class DateUtil:

    @classmethod
    def get_now_date(cls) -> str:
        return cls.datetime_to_str(datetime.datetime.now())

    @staticmethod
    def datetime_to_str(datetime_stamp: datetime.datetime) -> str:
        return datetime_stamp.strftime("%Y-%m-%d")

    @staticmethod
    def get_year_between_dates(from_date: Union[datetime.datetime, datetime.date],
                               to_date: Union[datetime.datetime, datetime.date]) -> int:
        """获取两个日期之间的年份"""
        return relativedelta(from_date, to_date).years
