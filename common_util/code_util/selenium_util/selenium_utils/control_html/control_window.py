import logging
import re
import time
import typing

from selenium import webdriver, common

from ..control_browser.control_browser import ControlBrowser
from ..entity.selenium_config import SeleniumConfig


class ControlWindow:

    @classmethod
    def close_other_window(cls, selenium_config: SeleniumConfig, window_titles: typing.Union[str, typing.List[str]]):
        """关闭其他窗口"""
        driver = ControlBrowser.get_driver(selenium_config)
        window_titles = [window_titles] if isinstance(window_titles, str) else window_titles
        for window_handle in driver.window_handles:
            try:
                cls.__switch_to_window(driver, window_handle)
            except common.exceptions.NoSuchWindowException:
                continue
            title = cls.get_title(selenium_config)
            for window_title in window_titles:
                if window_title and re.search(window_title, title):
                    break
                elif not window_title and window_title == title:
                    break
            else:
                logging.info(f"关闭窗口: {title}")
                driver.close()
        # 关闭完窗口之后还需要重新切换一下窗口
        cls.switch_window(selenium_config, window_titles[-1])

    @classmethod
    def confirm_alert(cls, selenium_config: SeleniumConfig):
        """确定alert弹窗"""
        driver = ControlBrowser.get_driver(selenium_config)
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
    def get_title(cls, selenium_config: SeleniumConfig) -> str:
        """获取标题"""
        driver = ControlBrowser.get_driver(selenium_config)
        try:
            return driver.title
        except common.UnexpectedAlertPresentException:
            cls.confirm_alert(selenium_config)
            return driver.title

    @classmethod
    def switch_window(cls, selenium_config: SeleniumConfig, window_title: str):
        """切换窗口"""
        driver = ControlBrowser.get_driver(selenium_config)
        for _ in range(max((selenium_config.wait_seconds // len(driver.window_handles)), 1)):
            target_handles = []
            for window_handle in driver.window_handles:
                try:
                    cls.__switch_to_window(driver, window_handle)
                except common.exceptions.NoSuchWindowException:
                    continue
                # 校验标题
                title = cls.get_title(selenium_config)
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
                if selenium_config.without_log:
                    continue
                logging.warning("指定的窗口数量为空，重新查询")
            else:
                cls.__switch_to_window(driver, target_handles[-1])
                raise RuntimeWarning(f"出现多个包含 {window_title} 的目标窗口")
        else:
            cls.__switch_to_window(driver, driver.window_handles[-1])  # 切换至最新窗口
            raise common.exceptions.NoSuchWindowException(f"未找到目标窗口: {window_title}")

    @staticmethod
    def __switch_to_window(driver: webdriver, window_handle: str):
        """切换到window中"""
        driver.switch_to.window(window_handle)
        # window切换完之后需要等待一小段时间再进行操作，不然可能会出现无法找到元素的情况
        time.sleep(0.5)
