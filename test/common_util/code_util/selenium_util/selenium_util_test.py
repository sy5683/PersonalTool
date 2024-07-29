from concurrent import futures

from common_core.base.test_base import TestBase
from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.selenium_util.selenium_utils.control_browser.browser_type import BrowserType
from common_util.code_util.selenium_util.selenium_utils.selenium_config import SeleniumConfig


class SeleniumUtilTestCase(TestBase):

    def setUp(self):
        self.url = "https://www.baidu.com/"
        self.xpath = '//map[@id="s_mp"]/area'
        self.title = "百度一下"

    def test_close_other_window(self):
        SeleniumUtil.close_other_window(window_titles=self.title)  # 关闭其他页签

    def test_click(self):
        # SeleniumUtil.click(self.xpath)  # 模拟点击，默认使用js点击
        SeleniumUtil.click(self.xpath, click_type='selenium')  # 使用selenium的点击方法

    def test_find(self):
        element = SeleniumUtil.find(self.xpath)  # 查找元素
        # element = SeleniumUtil.find(self.xpath, wait_seconds=30)  # 在指定超时时间内查找元素
        SeleniumUtil.find('./ancestor::div[id="lg"]', element=element)  # 查找父级元素

    def test_launch_chrome_debug(self):
        self.assertEqual(SeleniumUtil.launch_chrome_debug(), None)

    def test_open_url(self):
        SeleniumUtil.open_url(self.url)  # 打开url
        # SeleniumUtil.open_url(self.url, debug_port=9223)  # 接管debug浏览器打开url

    def test_thread(self):
        """测试多并发"""

        def _launch_driver():
            SeleniumUtil.open_url(self.url, use_user_data=False)  # 多并发时不能使用user_data
            print(SeleniumUtil.find('//input[@id="su"]', wait_seconds=20))
            SeleniumUtil.close_browser(driver=SeleniumUtil.get_driver())

        pool = futures.ThreadPoolExecutor(3, thread_name_prefix='test')
        tasks = []
        for _ in range(3):
            tasks.append(pool.submit(_launch_driver))
        for task in futures.as_completed(tasks):
            print(task.result())
