import datetime
import unittest

from personal_tool.work_tool.WorkReportFill.work_report_fill.feature.work_report.work_report_feature import \
    WorkReportFeature


class WorkReportFeatureTestCase(unittest.TestCase):

    def setUp(self):
        self.target_date = str(datetime.datetime.now())

    def test_get_now_weekly_report(self):
        now_weekly_report = WorkReportFeature.get_weekly_report(self.target_date)
        print(now_weekly_report.__dict__)

    def test_get_weekly_reports(self):
        weekly_reports = WorkReportFeature.get_weekly_reports()
        self.assertNotEqual(weekly_reports, None)
        for weekly_report in weekly_reports:
            print(weekly_report.__dict__)

    def test_get_work_report_path(self):
        work_report_path = WorkReportFeature._get_work_report_path()
        self.assertNotEqual(work_report_path, None)
        print(work_report_path)
