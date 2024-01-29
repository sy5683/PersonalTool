import datetime

from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from personal_tool.work_tool.工作报告填写器.feature.work_report.work_report_feature import WorkReportFeature


class WorkReportFeatureTestCase(TestBase):

    def setUp(self):
        self.target_date = str(datetime.datetime.now())

    def test_get_now_weekly_report(self):
        now_weekly_report = WorkReportFeature.get_weekly_report(self.target_date)
        ObjectUtil.print_object(now_weekly_report)

    def test_get_weekly_reports(self):
        weekly_reports = WorkReportFeature.get_weekly_reports()
        self.assertNotEqual(weekly_reports, None)
        for weekly_report in weekly_reports:
            ObjectUtil.print_object(weekly_report)

    def test_get_work_report_path(self):
        work_report_path = WorkReportFeature._get_work_report_path()
        self.assertNotEqual(work_report_path, None)
        print(work_report_path)
