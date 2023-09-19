import logging
import os
import tkinter
from pathlib import Path
from tkinter import filedialog
from typing import List

import openpyxl

from .entity.weekly_report import WeeklyReport
from .factory.daily_report_factory import DailyReportFactory
from ...util.time_util import TimeUtil


class WorkReportFeature:
    _work_report_path = str(Path(__file__).parent.parent.parent.joinpath("file\\日报.xlsx"))  # 工作报告默认地址

    @classmethod
    def get_now_weekly_report(cls) -> WeeklyReport:
        now_date = TimeUtil.get_now()
        weekly_reports = cls.get_weekly_reports()
        for weekly_report in reversed(weekly_reports):
            if now_date in weekly_report.date_range:
                return weekly_report
        raise Exception(f"未找到当前日期所在的周报: {now_date}")

    @classmethod
    def get_weekly_reports(cls) -> List[WeeklyReport]:
        daily_report_path = cls._get_work_report_path()
        wb = openpyxl.load_workbook(daily_report_path)
        weekly_reports = []
        weekly_report = None
        for rows in list(wb.active.iter_rows())[1:]:  # 去除表头
            row_values = [row.value for row in rows]
            if not any(row_values):  # 去除间隔行
                continue
            if row_values[1] == "周计划":
                weekly_report = WeeklyReport(row_values[2])
                weekly_reports.append(weekly_report)
            else:
                if weekly_report is None:
                    continue
                daily_report = DailyReportFactory.row_values_to_daily_report(row_values)
                weekly_report.add_daily_report(daily_report)
        wb.close()
        return weekly_reports

    @classmethod
    def _get_work_report_path(cls) -> str:
        if cls._work_report_path:
            if not os.path.exists(cls._work_report_path):
                logging.warning(f"默认日报文件路径不存在: {cls._work_report_path}")
                cls._work_report_path = None  # 重置为None，然后使用tkinter窗口重新获取
        if cls._work_report_path is None:
            tkinter.Tk().withdraw()  # 隐藏tk窗口
            cls._work_report_path = filedialog.askopenfilename()
        return cls._work_report_path
