import typing

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class ControlElement:
    """控制元素"""

    @staticmethod
    def find_element(element: typing.Union[WebDriver, WebElement], xpath: str, wait_seconds: int) -> WebElement:
        """查找元素"""
        return WebDriverWait(element, wait_seconds, 0.3).until(lambda x: x.find_element(By.XPATH, xpath))

    @staticmethod
    def find_elements(element: typing.Union[WebDriver, WebElement], xpath: str,
                      wait_seconds: int) -> typing.List[WebElement]:
        """查找元素列表"""
        return WebDriverWait(element, wait_seconds, 0.3).until(lambda x: x.find_elements(By.XPATH, xpath))

    @classmethod
    def get_attribute(cls, element: typing.Union[WebDriver, WebElement], xpath: str, parameter: str,
                      wait_seconds: int) -> str:
        """获取元素参数"""
        if xpath:
            element = cls.find_element(element, xpath, wait_seconds)
        else:
            if isinstance(element, WebDriver):
                raise TypeError("WebDriver无法使用get_attribute方法")
        return element.get_attribute(parameter)
