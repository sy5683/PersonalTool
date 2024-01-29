import datetime

from common_core.base.tool_base import ToolBase
from feature.oa.oa_feature import OaFeature
from feature.work_report.work_report_feature import WorkReportFeature


class WorkReportFiller(ToolBase):

    def __init__(self, target_date: str = str(datetime.datetime.now())):
        self.weekly_report = WorkReportFeature.get_weekly_report(target_date)

    def main(self):
        # 1) 登录OA
        OaFeature.login_oa()
        # 2) 切换至日报界面
        OaFeature.switch_in_report_page()
        # 3) 填写工作报告
        OaFeature.fill_report(self.weekly_report.daily_reports)


if __name__ == '__main__':
    work_report_filler = WorkReportFiller()
    work_report_filler.main()
