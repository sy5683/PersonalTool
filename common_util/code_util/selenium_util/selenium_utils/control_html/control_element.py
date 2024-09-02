import logging
import time
import traceback
import typing

from selenium import webdriver, common
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from ..control_browser.control_browser import ControlBrowser
from ..selenium_config import SeleniumConfig


class ControlElement:
    """控制元素"""

    @classmethod
    def click(cls, key: typing.Union[str, WebElement], **kwargs):
        """调用js实现模拟点击"""
        click_type = kwargs.get("click_type", "js")
        driver = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        wait_seconds = kwargs.get("wait_seconds", SeleniumConfig.wait_seconds)
        if click_type == "js":
            element = cls.__format_element(key, **kwargs)
            driver.execute_script("(arguments[0]).click()", element)
        elif click_type == "action":
            element = cls.__format_element(key, **kwargs)
            ActionChains(ControlBrowser.get_driver(**kwargs)).move_to_element(element).click().perform()
        else:
            kwargs['wait_seconds'] = 1
            for _ in range(wait_seconds):
                time.sleep(0.2)
                try:
                    cls.__format_element(key, **kwargs).click()
                except common.ElementNotInteractableException:
                    continue
                break
            else:
                raise common.ElementNotInteractableException("点击失败")

    @classmethod
    def exist(cls, xpath: str, **kwargs) -> bool:
        """查找元素"""
        try:
            cls.find(xpath, **kwargs)
        except common.TimeoutException:
            return False
        return True

    @classmethod
    def find(cls, xpath: str, **kwargs) -> WebElement:
        """查找元素"""
        if not kwargs.get("without_log"):
            logging.info(f"查找元素: {xpath}")
        return cls.__find_with_lambda(lambda x: x.find_element(By.XPATH, xpath), **kwargs)

    @classmethod
    def finds(cls, xpath: str, **kwargs) -> typing.List[WebElement]:
        """查找元素列表"""
        if not kwargs.get("without_log"):
            logging.info(f"查找元素列表: {xpath}")
        return cls.__find_with_lambda(lambda x: x.find_elements(By.XPATH, xpath), **kwargs)

    @classmethod
    def get_attribute(cls, key: typing.Union[str, WebElement], attribute_type: str, **kwargs) -> str:
        """
        获取元素内容
        :param key:
        :param attribute_type: 常用的值有: id, class, value, innerText
        :param kwargs:
        :return:
        """
        return cls.__format_element(key, **kwargs).get_attribute(attribute_type)

    @classmethod
    def input(cls, key: typing.Union[None, str, WebElement], value: str, **kwargs):
        """输入"""
        if key is None:
            if value not in Keys.__dict__.values():
                raise ValueError("未指定输入对象时，输入值必须为类Keys。")
            ActionChains(ControlBrowser.get_driver(**kwargs)).key_down(value).perform()
        else:
            element = cls.__format_element(key, **kwargs)
            logging.info(f"输入元素: {key} 【%s】" % ("*" * len(value) if cls.__check_is_password(element) else value))
            uncheck = kwargs.get("uncheck")
            for _ in range(3):
                # 先点击元素定位
                cls._clear_element(element)
                # 模拟全选
                element.send_keys(Keys.CONTROL, "a")
                time.sleep(0.2)
                # 输入元素
                element.send_keys(value)
                # 密码无需判断输入结果
                if cls.__check_is_password(element):
                    break
                # 某些特殊情况无需判断输入结果: 日期格式化、金额会计格式化等
                if uncheck:
                    break
                # 判断输入结果是否正确
                if element.get_attribute("value") == value:
                    break
            else:
                logging.error(f"元素输入失败: {key}\n{traceback.format_exc()}")
                raise RuntimeError("元素输入失败")

    @classmethod
    def select(cls, key: typing.Union[str, WebElement], value: typing.Union[int, str], **kwargs):
        """选择下拉选项"""
        element = cls.__format_element(key, **kwargs)
        select = Select(element)  # 实例化Select
        if isinstance(value, int):
            select.select_by_index(value)  # 根据项选择下拉选项
        else:
            try:
                select.select_by_visible_text(value)  # 根据可见文本选择下拉选项
            except common.NoSuchElementException:
                select.select_by_value(value)  # 根据值选择下拉选项

    @classmethod
    def wait_disappear(cls, key: typing.Union[str, WebElement], **kwargs) -> bool:
        """
        等待元素消失
        需要注意的是，检测元素消失的前提是这个元素已经出现
        使用时需要注意，不要在做完上一个操作之后立马调用这个方法，不然可能会出现【要检测消失的元素还未出现，这个方法就已经判断该元素已消失】
        在使用时需要根据具体情况在前面加一定时间的强制等待
        """
        wait_seconds = kwargs.get("wait_seconds", SeleniumConfig.wait_seconds)
        kwargs['wait_seconds'] = 1
        time.sleep(1)
        for _ in range(wait_seconds):
            try:
                element = cls.__format_element(key, **kwargs)
                print(element.text)  # 这一行是为了检测入参为WebElement的元素
            except (common.exceptions.NoSuchElementException, common.exceptions.TimeoutException):
                return True
            finally:
                time.sleep(1)
        return False

    @staticmethod
    def _clear_element(element: WebElement):
        """清空元素"""
        # 先点击再删除
        try:
            element.click()
        except common.ElementClickInterceptedException:
            logging.warning("元素无法点击，请选择正确的元素")
        time.sleep(0.5)
        # 使用selenium自带的clear方法
        try:
            element.clear()
        except common.InvalidElementStateException:
            logging.warning("元素无法清空，请选择正确的元素")
        time.sleep(0.5)
        # 有时候有输入框 element.clear() 方法无效，因此再使用手动清空方式
        for _ in range(len(element.get_attribute("value"))):
            element.send_keys(Keys.RIGHT)
            element.send_keys(Keys.BACK_SPACE)
            time.sleep(0.1)

    @staticmethod
    def __check_is_password(element: WebElement) -> bool:
        """判断元素是否为密码类"""
        return element.get_attribute("type") == "password"

    @staticmethod
    def __find_with_lambda(find_method, **kwargs) -> typing.Union[WebElement, typing.List[WebElement]]:
        """显性等待查找元素"""
        element: typing.Union[webdriver, WebElement] = kwargs.get("element")
        wait_seconds = kwargs.get("wait_seconds", SeleniumConfig.wait_seconds)
        if element is None:
            element = kwargs.get("driver", ControlBrowser.get_driver(**kwargs))
        # 注！查询间隔为一秒时，这个方法无法检测等待时间为1秒的元素（检测次数为1，即即时检测，而不是预计的等待一秒后报错，因此这里将间隔时间修改为0.3s）
        return WebDriverWait(element, wait_seconds, 0.3).until(find_method)

    @classmethod
    def __format_element(cls, key: typing.Union[str, WebElement], **kwargs):
        return cls.find(xpath=key, **kwargs) if isinstance(key, str) else key
