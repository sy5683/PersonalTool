import datetime
from enum import Enum
from typing import Union

from dateutil.relativedelta import relativedelta


class TimeFormat(Enum):
    """日期格式"""
    stamp = {}
    full = {'format': "%Y-%m-%d %H:%M:%S"}
    chinese_full = {'format': "%Y{Y}%m{m}%d{d}%H{H}%M{M}%S{S}"}
    number_full = {'format': "%Y%m%d%H%M%S"}
    date = {'format': "%Y-%m-%d"}
    chinese_date = {'format': "%Y{Y}%m{m}%d{d}"}
    number_date = {'format': "%Y%m%d"}
    time = {'format': "%H:%M:%S"}
    chinese_time = {'format': "%H{H}%M{M}%S{S}"}
    number_time = {'format': "%H%M%S"}
    year_and_month = {'format': "%Y-%m"}
    chinese_year_and_month = {'format': "%Y{Y}%m{m}"}
    number_year_and_month = {'format': '%Y%m'}
    month_and_day = {'format': "%m-%d"}
    chinese_month_and_day = {'format': "%m{m}%d{d}"}
    number_month_and_day = {'format': "%m%d"}
    chinese_year = {'format': "%Y{Y}"}
    chinese_month = {'format': "%m{m}"}
    chinese_day = {'format': "%d{d}"}
    chinese_hour = {'format': "%H{H}"}
    chinese_minute = {'format': "%M{M}"}
    chinese_seconds = {'format': "%S{S}"}

    def to_format(self) -> str:
        return self.value['format']


class TimeUtil:

    @classmethod
    def get_now(cls, time_format: TimeFormat = TimeFormat.stamp) -> Union[datetime.datetime, str]:
        """获取当前时间"""
        now_stamp = datetime.datetime.now()
        return now_stamp if time_format == TimeFormat.stamp else cls.stamp_to_str(now_stamp, time_format)

    "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    @staticmethod
    def stamp_to_str(time_stamp: Union[str, datetime.datetime], time_format: TimeFormat = TimeFormat.full) -> str:
        """时间戳格式化为字符串"""
        if isinstance(time_stamp, str):
            return time_stamp
        assert time_format != TimeFormat.stamp
        return time_stamp.strftime(time_format.to_format()).format(Y="年", m="月", d="日", H="时", M="分", S="秒")

    @staticmethod
    def get_year_between_dates(from_date: Union[datetime.datetime, datetime.date],
                               to_date: Union[datetime.datetime, datetime.date]) -> int:
        """获取两个日期之间的年份"""
        return relativedelta(from_date, to_date).years
