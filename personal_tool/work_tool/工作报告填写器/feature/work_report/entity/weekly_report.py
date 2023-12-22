import datetime
import typing

from common_util.data_util.number_util.number_util import NumberUtil
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

    def set_completion_rates(self):
        """设置完成率"""
        rate = NumberUtil.divide_float(100, len(self.daily_reports))
        for index, daily_report in enumerate(self.daily_reports):
            daily_report.completion_rate = round(NumberUtil.multiply_float(index + 1, rate))
            # 最后一个日报完成率设为100%
            if daily_report == self.daily_reports[-1]:
                daily_report.completion_rate = 100
