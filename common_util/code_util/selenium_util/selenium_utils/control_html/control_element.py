from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class ControlElement:
    """控制元素"""

    @staticmethod
    def find_element(driver: webdriver, xpath: str, wait_seconds: float, interval: float = 0.3) -> WebElement:
        """显性等待查找元素"""
        # 注！查询间隔为一秒时，这个方法无法检测等待时间为1秒的元素（检测次数为1，即即时检测，而不是预计的等待一秒后报错）
        return WebDriverWait(driver, wait_seconds, interval).until(lambda x: x.find_element(By.XPATH, xpath))
