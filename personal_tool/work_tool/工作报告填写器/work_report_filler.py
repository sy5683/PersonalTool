import datetime

from feature.work_report.work_report_feature import WorkReportFeature


class WorkReportFiller:

    def __init__(self, target_date: str = str(datetime.datetime.now())):
        self.target_date = target_date

    def main(self):
        weekly_report = WorkReportFeature.get_weekly_report(self.target_date)
        for daily_report in weekly_report.daily_reports:
            print("\n==============================\n")
            print(daily_report.to_report())


if __name__ == '__main__':
    work_report_filler = WorkReportFiller()
    work_report_filler.main()
