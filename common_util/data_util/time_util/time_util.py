import datetime
import typing

from .time_utils.calculate_datetime import CalculateDatetime
from .time_utils.convert_time import ConvertTime
from .time_utils.time_config import TimeConfig


class TimeUtil:

    @staticmethod
    def format_to_datetime(stamp: typing.Union[datetime.datetime, datetime.date, float, str]) -> datetime.datetime:
        """格式化为datetime"""
        return ConvertTime.format_to_datetime(stamp)

    @staticmethod
    def format_to_str(stamp: typing.Union[datetime.datetime, datetime.date, float, str],
                      time_format: str = TimeConfig.default_time_format) -> str:
        """格式时间"""
        return ConvertTime.format_to_str(stamp, time_format)

    @staticmethod
    def get_days_between_dates(from_date: typing.Union[datetime.datetime, datetime.date, str],
                               to_date: typing.Union[datetime.datetime, datetime.date, str]) -> int:
        """获取两个日期之间的天数"""
        return CalculateDatetime.get_days_between_dates(from_date, to_date)

    @staticmethod
    def get_last_month_first_day(stamp: typing.Union[datetime.datetime, datetime.date, str]) -> datetime.date:
        """获取指定月份上个月的第一天日期"""
        return CalculateDatetime.get_last_month_first_day(stamp)

    @staticmethod
    def get_last_month_last_day(stamp: typing.Union[datetime.datetime, datetime.date, str]) -> datetime.date:
        """获取指定月份上个月的最后一天日期"""
        return CalculateDatetime.get_last_month_last_day(stamp)

    @staticmethod
    def get_next_month_first_day(stamp: typing.Union[datetime.datetime, datetime.date, str]) -> datetime.date:
        """获取指定月份下个月的第一天日期"""
        return CalculateDatetime.get_next_month_first_day(stamp)

    @staticmethod
    def get_next_month_last_day(stamp: typing.Union[datetime.datetime, datetime.date, str]) -> datetime.date:
        """获取指定月份下个月的第一天日期"""
        return CalculateDatetime.get_next_month_last_day(stamp)

    @staticmethod
    def get_now(time_format: str = TimeConfig.default_time_format) -> str:
        """获取当前时间"""
        return ConvertTime.format_to_str(datetime.datetime.now(), time_format)

    @staticmethod
    def get_this_month_first_day(stamp: typing.Union[datetime.datetime, datetime.date, str]) -> datetime.date:
        """获取指定月份的第一天日期"""
        return CalculateDatetime.get_this_month_first_day(stamp)

    @staticmethod
    def get_this_month_last_day(stamp: typing.Union[datetime.datetime, datetime.date, str]) -> datetime.date:
        """获取指定月份的最后一天日期"""
        return CalculateDatetime.get_this_month_last_day(stamp)

    @staticmethod
    def get_years_between_dates(from_date: typing.Union[datetime.datetime, datetime.date, str],
                                to_date: typing.Union[datetime.datetime, datetime.date, str]) -> int:
        """获取两个日期之间的年份"""
        return CalculateDatetime.get_years_between_dates(from_date, to_date)
