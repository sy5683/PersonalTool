from common_core.base.tool_base import ToolBase
from feature.browser_checker import BrowserChecker
from feature.selenium_checker import SeleniumChecker


class ComputerChecker(ToolBase):

    def main(self, *args, **kwargs):
        # 1) 检测谷歌浏览器
        BrowserChecker.check_chrome_browser()
        # 2) 检测谷歌浏览器driver
        SeleniumChecker.check_chrome_driver()


if __name__ == '__main__':
    computer_checker = ComputerChecker()
    computer_checker.main()
