from common_core.base.test_base import TestBase
from common_util.code_util.playwright_util.playwright_util import PlaywrightUtil
from common_util.code_util.playwright_util.playwright_utils.entity.playwright_config import PlaywrightConfig
from common_util.code_util.selenium_util.selenium_util import SeleniumUtil


class PlaywrightUtilTestCase(TestBase):

    def setUp(self):
        self.url = "https://www.baidu.com/"
        self.xpath = '//*[@value="百度一下"]'
        self.title = "百度一下"
        self.debug_port = 9222

    def test_click(self):
        PlaywrightUtil.click(PlaywrightConfig(xpath=self.xpath))  # 模拟点击，默认使用js点击
        # PlaywrightUtil.click(PlaywrightConfig(xpath=self.xpath, operate_type=OperateType.selenium))  # 使用selenium的点击方法

    def test_find(self):
        locator = PlaywrightUtil.find(PlaywrightConfig(xpath=self.xpath))  # 查找元素
        print(locator)

    def test_launch_chrome_debug(self):
        # playwright的接管浏览器方法与selenium的相同，因此debug启动谷歌浏览器方法直接使用SeleniumUtil中的即可
        SeleniumUtil.launch_chrome_debug(self.debug_port)

    def test_open_url(self):
        PlaywrightUtil.open_url(PlaywrightConfig(), self.url)
        # # 接管debug浏览器打开url
        # PlaywrightUtil.open_url(PlaywrightConfig(debug_port=self.debug_port), self.url)
