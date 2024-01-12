import time

from ..control_browser.control_browser import ControlBrowser


class ControlDriver:

    @staticmethod
    def execute_js(js: str, **kwargs):
        """执行js代码"""
        driver = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        driver.execute_script(js)
        time.sleep(1)  # 执行结束之后等待一秒
