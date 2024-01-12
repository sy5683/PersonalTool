import unittest

from personal_tool.work_tool.工作报告填写器.feature.oa.oa_feature import OaFeature


class OaFeatureTestCase(unittest.TestCase):
    def test_submit_report(self):
        self.assertEqual(OaFeature.submit_report(), None)
