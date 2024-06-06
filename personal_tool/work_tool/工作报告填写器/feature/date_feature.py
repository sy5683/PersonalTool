import datetime
import typing

from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from .config import WorkReportFillerConfig


class DateFeature:

    @staticmethod
    def format_date(stamp: typing.Union[datetime.datetime, float, str]) -> str:
        """格式化日期"""
        return TimeUtil.format_to_str(ExcelUtil.format_date_data(stamp), WorkReportFillerConfig.time_format)

    @staticmethod
    def get_now_date() -> str:
        """获取当前日期"""
        return TimeUtil.get_now(WorkReportFillerConfig.time_format)
