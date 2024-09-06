import logging
import time

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig


class BrowserChecker:

    @staticmethod
    def check_chrome_browser():
        """检测谷歌浏览器"""
        logging.info("检测谷歌浏览器是否更新")
        SeleniumUtil.open_url(SeleniumConfig(), "chrome://settings/help")
        # 死循环保证窗口运行，直到手动关闭窗口终止脚本
        while True:
            try:
                SeleniumUtil.find(SeleniumConfig(xpath='//settings-ui', without_log=True))
            except Exception as e:
                logging.warning(e)
                time.sleep(3)
                break
