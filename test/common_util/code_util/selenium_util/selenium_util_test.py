from concurrent import futures

from common_core.base.test_base import TestBase
from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig
from common_util.code_util.selenium_util.selenium_utils.enum.operate_type import OperateType


class SeleniumUtilTestCase(TestBase):

    def setUp(self):
        self.url = "https://www.baidu.com/"
        self.xpath = '//map[@id="s_mp"]/area'
        self.title = "百度一下"
        self.debug_port = 9222

    def test_close_other_window(self):
        SeleniumUtil.close_other_window(SeleniumConfig(), self.title)  # 关闭其他页签

    def test_click(self):
        # SeleniumUtil.click(SeleniumConfig(xpath=self.xpath))  # 模拟点击，默认使用js点击
        SeleniumUtil.click(SeleniumConfig(xpath=self.xpath, operate_type=OperateType.selenium))  # 使用selenium的点击方法

    def test_find(self):
        element = SeleniumUtil.find(SeleniumConfig(xpath=self.xpath))  # 查找元素
        # element = SeleniumUtil.find(SeleniumConfig(xpath=self.xpath, wait_seconds=30))  # 在指定超时时间内查找元素
        SeleniumUtil.find(SeleniumConfig(xpath='./ancestor::div[@id="lg"]', element=element))  # 查找父级元素

    def test_launch_chrome_debug(self):
        SeleniumUtil.launch_chrome_debug(self.debug_port)

    def test_open_url(self):
        SeleniumUtil.open_url(SeleniumConfig(), self.url)
        # # 接管debug浏览器打开url
        # SeleniumUtil.open_url(SeleniumConfig(debug_port=self.debug_port), self.url)
        # # 指定driver打开url
        # driver_path = SeleniumUtil.get_chrome_driver_path()
        # SeleniumUtil.open_url(SeleniumConfig(driver_path=driver_path), self.url)

    def test_thread(self):
        """测试多并发"""

        def _launch_driver():
            SeleniumUtil.open_url(SeleniumConfig(use_user_data=False), self.url)  # 多并发时不能使用user_data
            print(SeleniumUtil.find(SeleniumConfig(xpath='//input[@id="su"]', wait_seconds=20)))
            driver = SeleniumUtil.get_driver(SeleniumConfig())
            SeleniumUtil.close_browser(SeleniumConfig(driver=driver))

        pool = futures.ThreadPoolExecutor(3, thread_name_prefix='test')
        tasks = []
        for _ in range(3):
            tasks.append(pool.submit(_launch_driver))
        for task in futures.as_completed(tasks):
            print(task.result())
