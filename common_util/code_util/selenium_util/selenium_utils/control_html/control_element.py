import logging
import time
import traceback
import typing

from selenium import webdriver
from selenium.common import InvalidElementStateException, TimeoutException, ElementNotInteractableException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from ..control_browser.control_browser import ControlBrowser
from ..selenium_config import SeleniumConfig


class ControlElement:
    """控制元素"""

    @classmethod
    def click(cls, element_or_xpath: typing.Union[WebElement, str], **kwargs):
        """调用js实现模拟点击"""
        click_type = kwargs.get("click_type", "js")
        driver = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        wait_seconds = kwargs.get("wait_seconds", SeleniumConfig.wait_seconds)
        if click_type == "js":
            element = cls.__format_element(element_or_xpath, wait_seconds=wait_seconds)
            driver.execute_script("(arguments[0]).click()", element)
            time.sleep(0.2)
        else:
            for _ in range(wait_seconds):
                time.sleep(1)
                try:
                    cls.__format_element(element_or_xpath, wait_seconds=1).click()
                except ElementNotInteractableException:
                    continue
                break
            else:
                raise ElementNotInteractableException("点击失败")

    @classmethod
    def exist(cls, xpath: str, **kwargs) -> bool:
        """查找元素"""
        try:
            cls.find(xpath, **kwargs)
        except TimeoutException:
            return False
        return True

    @classmethod
    def find(cls, xpath: str, **kwargs) -> WebElement:
        """查找元素"""
        logging.info(f"查找元素: {xpath}")
        return cls.__find_with_lambda(lambda x: x.find_element(By.XPATH, xpath), xpath, **kwargs)

    @classmethod
    def finds(cls, xpath: str, **kwargs) -> typing.List[WebElement]:
        """查找元素列表"""
        logging.info(f"查找元素列表: {xpath}")
        return cls.__find_with_lambda(lambda x: x.find_elements(By.XPATH, xpath), xpath, **kwargs)

    @classmethod
    def input(cls, element_or_xpath: typing.Union[WebElement, str], value: str, **kwargs):
        """输入"""
        element = cls.__format_element(element_or_xpath, **kwargs)
        logging.info(f"输入元素: {element_or_xpath} 【%s】" %
                     ("*" * len(value) if cls.__check_element_is_password(element) else value))
        for _ in range(3):
            # 先点击元素定位
            element.click()
            time.sleep(0.5)
            # 使用selenium自带的clear方法
            try:
                element.clear()  # 有时候有输入框 element.clear() 方法无效
            except InvalidElementStateException:
                logging.warning("元素无法清空，请选择正确的元素")
            time.sleep(0.5)
            # 因此再使用手动清空方式
            for _ in range(len(element.get_attribute("value"))):
                element.send_keys(Keys.RIGHT)
                element.send_keys(Keys.BACK_SPACE)
                time.sleep(0.1)
            # 输入元素
            element.send_keys(value)
            # 密码无需判断输入结果
            if cls.__check_element_is_password(element):
                break
            # 某些特殊情况无需判断输入结果: 日期格式化、金额会计格式化等
            if kwargs.get("uncheck"):
                break
            # 判断输入结果是否正确
            if element.get_attribute("value") == value:
                break
        else:
            logging.error(f"元素输入失败: {element_or_xpath}\n{traceback.format_exc()}")
            raise RuntimeError("元素输入失败")

    @staticmethod
    def __find_with_lambda(find_method, xpath: str, **kwargs) -> typing.Union[WebElement, typing.List[WebElement]]:
        """显性等待查找元素"""
        element: typing.Union[webdriver, WebElement] = kwargs.get("element")
        if element is None:
            element = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        if isinstance(element, WebElement):
            assert xpath.startswith("./"), f"WebElement的查询xpath需要以./开头: {xpath}"
        wait_seconds = kwargs.get("wait_seconds", SeleniumConfig.wait_seconds)
        # 注！查询间隔为一秒时，这个方法无法检测等待时间为1秒的元素（检测次数为1，即即时检测，而不是预计的等待一秒后报错，因此这里将间隔时间修改为0.3s）
        return WebDriverWait(element, wait_seconds, 0.3).until(find_method)

    @classmethod
    def __format_element(cls, element_or_xpath: typing.Union[WebElement, str], **kwargs):
        return cls.find(xpath=element_or_xpath, **kwargs) if isinstance(element_or_xpath, str) else element_or_xpath

    @staticmethod
    def __check_element_is_password(element: WebElement) -> bool:
        """判断元素是否为密码类"""
        return element.get_attribute("type") == "password"
