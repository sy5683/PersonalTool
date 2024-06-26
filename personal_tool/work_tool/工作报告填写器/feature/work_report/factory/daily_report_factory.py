import datetime
import typing

from ..entity.daily_report import DailyReport
from ...date_feature import DateFeature


class DailyReportFactory:

    @staticmethod
    def row_values_to_daily_report(row_values: typing.List[typing.Union[datetime.datetime, str]]) -> DailyReport:
        daily_report = DailyReport()
        daily_report.date = DateFeature.format_date(row_values[1])  # 日期
        daily_report.today_work = "" if row_values[2] is None else row_values[2]  # 今日工作
        daily_report.tomorrow_plan = "" if row_values[3] is None else row_values[3]  # 明日计划
        return daily_report
