from selenium import webdriver
from selenium.common import NoSuchWindowException, UnexpectedAlertPresentException


class ControlWindow:
    """控制窗口"""

    # @staticmethod
    # def get_title(driver: webdriver) -> str:
    #     """获取标题"""
    #     try:
    #         return SeleniumSource.get_title(driver)
    #     except UnexpectedAlertPresentException:
    #         # 如果出现弹窗时，获取标题会失败，因此这里特殊处理一下，先点击完弹窗再获取标题
    #         SeleniumSource.confirm_alert(driver)
    #         TimeSource.time_sleep(1)
    #         return SeleniumSource.get_title(driver)
    #
    # @classmethod
    # def switch_window(cls, driver: webdriver, window_title: str, wait_seconds: int):
    #     """切换窗口"""
    #     window_handles = SeleniumSource.get_window_handles(driver)
    #     for _ in range(max((wait_seconds // len(window_handles)), 1)):
    #         target_handles = []
    #         for window_handle in SeleniumSource.get_window_handles(driver):
    #             try:
    #                 cls._switch_to_window(driver, window_handle)
    #             except NoSuchWindowException:
    #                 continue
    #             title = cls.get_title(driver)
    #             if window_title:
    #                 if not ReSource.re_search(window_title, title):
    #                     continue
    #             else:
    #                 if title:
    #                     continue
    #             target_handles.append(window_handle)
    #         if not target_handles:
    #             continue
    #         if len(target_handles) == 1:
    #             cls._switch_to_window(driver, target_handles[0])
    #             break
    #         else:
    #             driver.switch_to.window(target_handles[-1])
    #             raise ElementFindError(f"出现多个包含【{window_title}】的目标窗口")
    #
    #     else:
    #         SeleniumSource.switch_to_window(driver, window_handles[-1])
    #         raise ElementFindError(f"未找到目标窗口: {window_title}")
    #
    # @staticmethod
    # def _switch_to_window(driver: webdriver, window_handle: str):
    #     """切换到window中"""
    #     SeleniumSource.switch_to_window(driver, window_handle)
    #     # window切换完之后需要等待一小段时间再进行操作，不然可能会出现无法找到元素的情况
    #     TimeSource.time_sleep(1)
