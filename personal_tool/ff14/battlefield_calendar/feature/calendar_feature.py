import calendar
import datetime
from typing import List, Tuple


class CalendarFeature:

    @classmethod
    def get_calendar_list(cls, year: int, month: int) -> List[datetime.date]:
        last_year, last_month = cls._get_last_year_and_month(year, month)
        last_month_calendar = cls.get_month_calendar(last_year, last_month)
        for day in list(last_month_calendar)[-1]:
            if not day:
                continue
            yield datetime.date(last_year, last_month, int(day))
        now_month_calendar = cls.get_month_calendar(year, month)
        for week in now_month_calendar:
            for day in week:
                if not day:
                    continue
                yield datetime.date(year, month, int(day))
        next_year, next_month = cls._get_next_year_and_month(year, month)
        next_month_calendar = cls.get_month_calendar(next_year, next_month)
        for day in list(next_month_calendar)[0]:
            if not day:
                continue
            yield datetime.date(next_year, next_month, int(day))

    @staticmethod
    def get_month_calendar(year: int, month: int) -> List[str]:
        """获取指定月份日历"""
        calendar_full = calendar.month(year, month)
        calendar_table, calendar_tag, calendar_only = calendar_full.split("\n", 2)
        for index, week_calendar in enumerate(calendar_only.split("\n")):
            week_calendar_list = [each for each in week_calendar.split(" ") if each]
            if not week_calendar_list:
                continue
            if not index:
                week_calendar_list = ([""] * 7 + week_calendar_list)[-7:]
            else:
                week_calendar_list = (week_calendar_list + [""] * 7)[:7]
            yield week_calendar_list

    @staticmethod
    def _get_last_year_and_month(year: int, month: int) -> Tuple[int, int]:
        if month == 1:
            return year - 1, 12
        else:
            return year, month - 1

    @staticmethod
    def _get_next_year_and_month(year: int, month: int) -> Tuple[int, int]:
        if month == 12:
            return year + 1, 1
        else:
            return year, month + 1
