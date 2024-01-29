from common_core.base.test_base import TestBase
from personal_tool.work_tool.工作报告填写器.feature.oa.oa_feature import OaFeature


class OaFeatureTestCase(TestBase):

    def test_login_oa(self):
        self.assertEqual(OaFeature.login_oa(), None)

    def test_switch_in_report_page(self):
        self.assertEqual(OaFeature.switch_in_report_page(), None)
