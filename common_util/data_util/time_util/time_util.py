import datetime
import typing

from .time_utils.calculate_datetime import CalculateDatetime
from .time_utils.convert_datetime import ConvertDatetime
from .time_utils.convert_time import ConvertTime


class TimeUtil:

    @staticmethod
    def get_last_month_first_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份上个月的第一天日期"""
        return CalculateDatetime.get_last_month_first_day(stamp)

    @staticmethod
    def get_last_month_last_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份上个月的最后一天日期"""
        return CalculateDatetime.get_last_month_last_day(stamp)

    @staticmethod
    def get_next_month_first_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份下个月的第一天日期"""
        return CalculateDatetime.get_next_month_first_day(stamp)

    @staticmethod
    def get_next_month_last_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份下个月的第一天日期"""
        return CalculateDatetime.get_next_month_last_day(stamp)

    @staticmethod
    def get_now(**kwargs):
        """获取当前时间"""
        return ConvertDatetime.format_time(str(datetime.datetime.now()), **kwargs)

    @staticmethod
    def get_this_month_first_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份的第一天日期"""
        return CalculateDatetime.get_this_month_first_day(stamp)

    @staticmethod
    def get_this_month_last_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份的最后一天日期"""
        return CalculateDatetime.get_this_month_last_day(stamp)

    @staticmethod
    def get_year_between_dates(from_date: typing.Union[datetime.datetime, datetime.date],
                               to_date: typing.Union[datetime.datetime, datetime.date]) -> int:
        """获取两个日期之间的年份"""
        return CalculateDatetime.get_year_between_dates(from_date, to_date)

    @staticmethod
    def format_time(time_str: str, **kwargs) -> str:
        """格式时间"""
        return ConvertDatetime.format_time(time_str, **kwargs)

    @staticmethod
    def time_to_datetime(stamp: float) -> datetime.datetime:
        """时间戳转datetime"""
        return ConvertTime.time_to_datetime(stamp)
