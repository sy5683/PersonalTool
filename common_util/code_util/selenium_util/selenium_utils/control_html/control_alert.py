import time

from ..control_browser.control_browser import ControlBrowser


class ControlAlert:

    @staticmethod
    def confirm_alert(**kwargs):
        """确认弹窗"""
        driver = ControlBrowser.get_driver(**kwargs)
        # 遍历页面，关闭弹窗
        for window_handle in driver.window_handles:
            # noinspection PyBroadException
            try:
                driver.switch_to.window(window_handle)
                time.sleep(0.5)
                driver.switch_to.alert.accept()
            except Exception:
                pass
