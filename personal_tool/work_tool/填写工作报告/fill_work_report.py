import datetime

from feature.work_report.work_report_feature import WorkReportFeature


class FillWorkReport:

    def __init__(self, target_date: str = str(datetime.datetime.now())):
        self.target_date = target_date

    def main(self):
        weekly_report = WorkReportFeature.get_weekly_report(self.target_date)
        for daily_report in weekly_report.daily_reports:
            print(daily_report.to_report())
            print("\n==============================\n")


if __name__ == '__main__':
    fill_work_report = FillWorkReport()
    fill_work_report.main()
