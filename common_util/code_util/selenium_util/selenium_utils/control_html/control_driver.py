import time

from ..control_browser.control_browser import ControlBrowser
from ..entity.selenium_config import SeleniumConfig


class ControlDriver:

    @staticmethod
    def execute_js(selenium_config: SeleniumConfig, js: str):
        """执行js代码"""
        driver = ControlBrowser.get_driver(selenium_config)
        driver.execute_script(js)
        time.sleep(1)  # 执行结束之后等待一秒

    @staticmethod
    def open_url(selenium_config: SeleniumConfig, url: str):
        """打开url"""
        for _ in range(3):
            try:
                return ControlBrowser.get_driver(selenium_config).get(url)
            except OSError:
                # selenium驱动升级会导致driver失效，会报错OSError
                selenium_config.info("selenium启动异常，重新启动")
