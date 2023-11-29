import datetime
import typing

from .daily_report import DailyReport


class WeeklyReport:
    """周报"""

    def __init__(self, weekly_plan: str):
        self.weekly_plan = weekly_plan  # 周计划
        self.daily_reports: typing.List[DailyReport] = []  # 日报列表
        self.date_range: typing.List[datetime.datetime] = []  # 日期区间

    def add_daily_report(self, daily_report: DailyReport):
        self.daily_reports.append(daily_report)
        self.date_range.append(daily_report.date)
