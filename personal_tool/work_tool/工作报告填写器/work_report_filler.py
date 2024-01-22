import datetime

from feature.oa.oa_feature import OaFeature
from feature.work_report.work_report_feature import WorkReportFeature


class WorkReportFiller:

    def __init__(self, target_date: str = str(datetime.datetime.now())):
        self.target_date = target_date

    def main(self):
        # 1) 获取周报
        weekly_report = WorkReportFeature.get_weekly_report(self.target_date)

        # 2.1) 登录OA
        OaFeature.login_oa()
        # 2.2) 切换至日报界面
        OaFeature.switch_in_report_page()
        # 2.3) 填写工作报告
        OaFeature.fill_report(weekly_report.daily_reports)


if __name__ == '__main__':
    work_report_filler = WorkReportFiller()
    work_report_filler.main()
