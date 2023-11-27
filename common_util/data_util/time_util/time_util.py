import datetime
import typing

from .time_utils.calculate_datetime import CalculateDatetime
from .time_utils.convert_datetime import ConvertDatetime


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
    def get_this_month_first_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份的第一天日期"""
        return CalculateDatetime.get_this_month_first_day(stamp)

    @staticmethod
    def get_this_month_last_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份的最后一天日期"""
        return CalculateDatetime.get_this_month_last_day(stamp)

    @staticmethod
    def get_next_month_first_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份下个月的第一天日期"""
        return CalculateDatetime.get_next_month_first_day(stamp)

    @staticmethod
    def get_next_month_last_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份下个月的第一天日期"""
        return CalculateDatetime.get_next_month_last_day(stamp)

    @staticmethod
    def format_time(time_str: str, time_format: str = '%Y{Y}%m{m}%d{d}%H{H}%M{M}%S{S}') -> str:
        """格式时间"""
        return ConvertDatetime.format_time(time_str, time_format)
