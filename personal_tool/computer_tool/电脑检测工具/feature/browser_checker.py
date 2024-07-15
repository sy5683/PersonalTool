import logging
import time

from selenium import common

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil


class BrowserChecker:

    @staticmethod
    def check_chrome_browser():
        """检测谷歌浏览器"""
        logging.info("检测谷歌浏览器是否更新")
        SeleniumUtil.open_url("chrome://settings/help")
        # 死循环保证窗口运行，直到手动关闭窗口终止脚本
        while True:
            try:
                SeleniumUtil.find('//settings-ui', without_log=True)
            except common.NoSuchWindowException:
                time.sleep(3)
                break
