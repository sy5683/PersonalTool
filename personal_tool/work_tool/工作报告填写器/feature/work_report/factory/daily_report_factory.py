import datetime
import typing

from common_util.file_util.excel_util.excel_util import ExcelUtil
from ..entity.daily_report import DailyReport
from ...config import WorkReportFillerConfig


class DailyReportFactory:

    @staticmethod
    def row_values_to_daily_report(row_values: typing.List[typing.Union[str, datetime.datetime]]) -> DailyReport:
        daily_report = DailyReport()
        daily_report.date = ExcelUtil.format_date_data(row_values[1], WorkReportFillerConfig.time_format)  # 日期
        daily_report.today_work = "" if row_values[2] is None else row_values[2]  # 今日工作
        daily_report.tomorrow_plan = "" if row_values[3] is None else row_values[3]  # 明日计划
        return daily_report
