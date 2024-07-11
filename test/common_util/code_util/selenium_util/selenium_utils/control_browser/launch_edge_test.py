from common_core.base.test_base import TestBase
from common_util.code_util.selenium_util.selenium_utils.control_browser.launch_browser.launch_edge import LaunchEdge


class LaunchEdgeTestCase(TestBase):

    def test_get_edge_path(self):
        edge_path = LaunchEdge._get_edge_path()
        self.assertNotEqual(edge_path, None)
        print(edge_path)

    def test_get_edge_user_data_path(self):
        user_data_path = LaunchEdge._get_edge_user_data_path()
        self.assertNotEqual(user_data_path, None)
        print(user_data_path)
