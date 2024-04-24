import logging
import time

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil


class BrowserChecker:

    @staticmethod
    def check_chrome_browser():
        """检测谷歌浏览器"""
        logging.info("检测谷歌浏览器是否更新")
        SeleniumUtil.open_url("chrome://settings/help")
        time.sleep(15)
