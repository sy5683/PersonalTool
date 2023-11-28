import datetime

from work_report_fill.feature.work_report.work_report_feature import WorkReportFeature


class WorkReportFill:
    """工作报告填写"""

    def __init__(self, target_date: str = str(datetime.datetime.now())):
        self.target_date = target_date

    def main(self):
        weekly_report = WorkReportFeature.get_weekly_report(self.target_date)
        for daily_report in weekly_report.daily_reports:
            print(daily_report.to_report())
            print("\n==============================\n")


if __name__ == '__main__':
    work_report_fill = WorkReportFill()
    work_report_fill.main()
