import datetime

from common_core.base.tool_base import ToolBase
from common_util.data_util.time_util.time_util import TimeUtil
from feature.config import WorkReportFillerConfig
from feature.oa.oa_feature import OaFeature
from feature.work_report.work_report_feature import WorkReportFeature


class WorkReportFiller(ToolBase):

    def __init__(self, target_date: str = str(datetime.datetime.now())):
        target_date = TimeUtil.format_to_str(target_date, WorkReportFillerConfig.time_format)
        self.weekly_report = WorkReportFeature.get_weekly_report(target_date)

    def main(self):
        if TimeUtil.get_now(WorkReportFillerConfig.time_format) in self.weekly_report.date_range:
            # 1.1) 登录OA
            OaFeature.login_oa()
            # 1.2) 切换至日报界面
            OaFeature.switch_in_report_page()
            # 1.3) 填写工作报告
            OaFeature.fill_reports(self.weekly_report.daily_reports)
        else:
            # 2) 目标日志为历史日志，不为当周。因此只将日志输出，自己手填
            for daily_report in self.weekly_report.daily_reports:
                print(f"【{daily_report.date}】")
                print(daily_report.to_report())
                print()


if __name__ == '__main__':
    work_report_filler = WorkReportFiller()
    work_report_filler.main()
