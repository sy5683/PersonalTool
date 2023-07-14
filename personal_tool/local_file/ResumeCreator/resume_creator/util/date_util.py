import datetime
from typing import Union

from dateutil.relativedelta import relativedelta


class DateUtil:

    @staticmethod
    def get_year_between_dates(from_date: Union[datetime.datetime, datetime.date],
                               to_date: Union[datetime.datetime, datetime.date]) -> int:
        """获取两个日期之间的年份"""
        return relativedelta(from_date, to_date).years
