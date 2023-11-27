import datetime
import typing

from dateutil.relativedelta import relativedelta


class CalculateDatetime:

    @classmethod
    def get_last_month_first_day(cls, stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份上个月的第一天日期"""
        last_month_last_day = cls.get_this_month_first_day(stamp) - datetime.timedelta(days=1)
        return datetime.date(last_month_last_day.year, last_month_last_day.month, 1)

    @classmethod
    def get_last_month_last_day(cls, stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份上个月的最后一天日期"""
        return cls.get_this_month_first_day(stamp) - datetime.timedelta(days=1)

    @staticmethod
    def get_next_month_first_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份下个月的第一天日期"""
        this_month_last_day = datetime.date(stamp.year, stamp.month, 28)  # 一个月最少28天
        for _ in range(4):  # 一个月最多31天，因此最多加四天到达下个月1号
            this_month_last_day += datetime.timedelta(days=1)
            if this_month_last_day.month != stamp.month:  # 月份不同时，说明已经为下个月日期
                return this_month_last_day

    @classmethod
    def get_next_month_last_day(cls, stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份下个月的第一天日期"""
        return cls.get_this_month_last_day(cls.get_next_month_first_day(stamp))

    @staticmethod
    def get_this_month_first_day(stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份的第一天日期"""
        return datetime.date(stamp.year, stamp.month, 1)

    @classmethod
    def get_this_month_last_day(cls, stamp: typing.Union[datetime.datetime, datetime.date]) -> datetime.date:
        """获取指定月份的最后一天日期"""
        return cls.get_next_month_first_day(stamp) - datetime.timedelta(days=1)

    @staticmethod
    def get_year_between_dates(from_date: typing.Union[datetime.datetime, datetime.date],
                               to_date: typing.Union[datetime.datetime, datetime.date]) -> int:
        """获取两个日期之间的年份"""
        return relativedelta(from_date, to_date).years
