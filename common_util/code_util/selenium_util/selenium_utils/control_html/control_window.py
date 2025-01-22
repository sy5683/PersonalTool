import re
import typing

from selenium import common

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
                driver.switch_to.window(window_handle)
            except common.exceptions.NoSuchWindowException:
                continue
            title = cls.get_title(selenium_config)
            for window_title in window_titles:
                if window_title and re.search(window_title, title):
                    break
                elif not window_title and window_title == title:
                    break
            else:
                # 需要注意，为了保证浏览器活性，当最后一个窗口仍不满足条件时，需要保留窗口
                if len(driver.window_handles) == 1:
                    raise RuntimeWarning(f"指定窗口不存在，将所有窗口关闭，保留一个窗口: {driver.title}")
                selenium_config.info(f"关闭窗口: {title}")
                driver.close()
        # 关闭完窗口之后还需要重新切换一下窗口
        cls.switch_window(selenium_config, window_titles[-1])

    @classmethod
    def confirm_alert(cls, selenium_config: SeleniumConfig):
        """确定alert弹窗"""
        driver = ControlBrowser.get_driver(selenium_config)
        # 遍历页面，关闭弹窗
        for window_handle in driver.window_handles:
            try:
                driver.switch_to.window(window_handle)
                driver.switch_to.alert.accept()
            except common.exceptions.NoSuchWindowException:
                pass

    @classmethod
    def get_title(cls, selenium_config: SeleniumConfig) -> str:
        """获取标题"""
        driver = ControlBrowser.get_driver(selenium_config)
        try:
            return driver.title
        except common.exceptions.UnexpectedAlertPresentException:
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
                    driver.switch_to.window(window_handle)
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
                selenium_config.info(f"切换到窗口: {driver.title if window_title else window_title}")
                driver.switch_to.window(target_handles[0])
                break
            elif not target_handles:
                selenium_config.info("指定的窗口数量为空，重新查询")
            else:
                driver.switch_to.window(target_handles[-1])
                raise common.exceptions.NoSuchWindowException(f"出现多个包含 {window_title} 的目标窗口")
        else:
            driver.switch_to.window(driver.window_handles[-1])  # 切换至最新窗口
            raise common.exceptions.NoSuchWindowException(f"未找到目标窗口: {window_title}")
