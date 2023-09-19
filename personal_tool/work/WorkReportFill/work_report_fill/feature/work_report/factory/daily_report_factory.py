import datetime
from typing import List, Union

from ..entity.daily_report import DailyReport
from ....util.time_util import TimeUtil


class DailyReportFactory:

    @staticmethod
    def row_values_to_daily_report(row_values: List[Union[str, datetime.datetime]]) -> DailyReport:
        daily_report = DailyReport()
        daily_report.date = TimeUtil.stamp_to_str(row_values[1])  # 日期
        daily_report.today_work = "" if row_values[2] is None else row_values[2]  # 今日工作
        daily_report.tomorrow_plan = "" if row_values[3] is None else row_values[3]  # 明日计划
        return daily_report
