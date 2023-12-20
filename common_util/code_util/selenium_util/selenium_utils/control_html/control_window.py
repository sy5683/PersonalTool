import logging
import re
import time
import typing

from selenium import webdriver
from selenium.common import NoSuchWindowException, UnexpectedAlertPresentException

from ..control_browser.control_browser import ControlBrowser
from ..selenium_config import SeleniumConfig


class ControlWindow:
    """控制窗口"""

    @classmethod
    def close_other_window(cls, window_titles: typing.Union[str, typing.List[str]], **kwargs):
        """关闭其他窗口"""
        window_titles = [window_titles] if isinstance(window_titles, str) else window_titles
        driver = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        for window_handle in driver.window_handles:
            try:
                cls.__switch_to_window(driver, window_handle)
            except NoSuchWindowException:
                continue
            title = cls.get_title(driver=driver)
            for window_title in window_titles:
                if window_title and re.search(window_title, title):
                    break
                elif not window_title and window_title == title:
                    break
            else:
                logging.info(f"关闭窗口: {title}")
                driver.close()
        # 关闭完窗口之后还需要重新切换一下窗口
        cls.switch_window(window_titles[-1])

    @classmethod
    def confirm_alert(cls, **kwargs):
        """确定alert弹窗"""
        driver = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        # 遍历页面，关闭弹窗
        for window_handle in driver.window_handles:
            # noinspection PyBroadException
            try:
                cls.__switch_to_window(driver, window_handle)
                driver.switch_to.alert.accept()
                time.sleep(0.5)
            except Exception:
                pass

    @classmethod
    def get_title(cls, **kwargs) -> str:
        """获取标题"""
        driver = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        try:
            return driver.title
        except UnexpectedAlertPresentException:
            cls.confirm_alert(driver=driver)
            return driver.title

    @classmethod
    def switch_window(cls, window_title: str, **kwargs):
        """切换窗口"""
        driver = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        wait_seconds = kwargs.get("wait_seconds", SeleniumConfig.default_debug_port)
        for _ in range(max((wait_seconds // len(driver.window_handles)), 1)):
            target_handles = []
            for window_handle in driver.window_handles:
                try:
                    cls.__switch_to_window(driver, window_handle)
                except NoSuchWindowException:
                    continue
                # 校验标题
                title = cls.get_title(driver=driver)
                if window_title and not re.search(window_title, title):
                    continue
                elif not window_title and window_title != title:
                    continue
                target_handles.append(window_handle)
            if len(target_handles) == 1:
                logging.info(f"切换到窗口: {driver.title if window_title else window_title}")
                cls.__switch_to_window(driver, target_handles[0])
                break
            elif not target_handles:
                logging.warning("指定的窗口数量为空，重新查询")
            else:
                cls.__switch_to_window(driver, target_handles[-1])
                raise Exception(f"出现多个包含 {window_title} 的目标窗口")
        else:
            cls.__switch_to_window(driver, driver.window_handles[-1])  # 切换至最新窗口
            raise Exception(f"未找到目标窗口: {window_title}")

    @staticmethod
    def __switch_to_window(driver: webdriver, window_handle: str):
        """切换到window中"""
        driver.switch_to.window(window_handle)
        # window切换完之后需要等待一小段时间再进行操作，不然可能会出现无法找到元素的情况
        time.sleep(0.5)
