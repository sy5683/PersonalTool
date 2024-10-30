import logging
import time
import traceback
import typing

from selenium import common
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from ..control_browser.control_browser import ControlBrowser
from ..entity.selenium_config import SeleniumConfig
from ..enum.operate_type import OperateType


class ControlElement:

    @classmethod
    def click(cls, selenium_config: SeleniumConfig):
        """模拟点击"""
        if selenium_config.operate_type == OperateType.action:
            cls.get_action(selenium_config).move_to_element(cls.find(selenium_config)).click().perform()
        elif selenium_config.operate_type == OperateType.js:
            cls.__get_driver(selenium_config).execute_script("(arguments[0]).click()", cls.find(selenium_config))
        else:
            wait_seconds = selenium_config.wait_seconds
            selenium_config.wait_seconds = 1
            for _ in range(wait_seconds):
                try:
                    cls.find(selenium_config).click()
                except common.ElementNotInteractableException:
                    continue
                break
            else:
                raise common.ElementNotInteractableException("点击失败")

    @classmethod
    def exist(cls, selenium_config: SeleniumConfig) -> bool:
        """查找元素是否存在"""
        try:
            element = cls.find(selenium_config) if selenium_config.element is None else selenium_config.element
            print(element.text)  # 这一行是为了检测入参为WebElement的元素
        except (AttributeError, common.TimeoutException):
            return False
        return True

    @classmethod
    def find(cls, selenium_config: SeleniumConfig) -> WebElement:
        """查找元素"""
        # 当存在xpath的情况下，优先定位xpath对应的元素
        if selenium_config.xpath:
            selenium_config.info(f"查找元素: {selenium_config.xpath}")
            return cls.__find(selenium_config, lambda x: x.find_element(By.XPATH, selenium_config.xpath))
        # 当xpath不存在的情况下，返回参数中的element，如果也为空，则需要报错
        if selenium_config.element is None:
            logging.error("参数中的xpath与element均为空，无法定位元素")
            raise AttributeError("传入的参数无法定位元素")
        return selenium_config.element

    @classmethod
    def finds(cls, selenium_config: SeleniumConfig) -> typing.List[WebElement]:
        """查找元素列表"""
        selenium_config.info(f"查找元素列表: {selenium_config.xpath}")
        return cls.__find(selenium_config, lambda x: x.find_elements(By.XPATH, selenium_config.xpath))

    @classmethod
    def get_action(cls, selenium_config: SeleniumConfig) -> ActionChains:
        """获取模拟操作动作"""
        return ActionChains(cls.__get_driver(selenium_config))

    @classmethod
    def get_attribute(cls, selenium_config: SeleniumConfig, attribute_type: str) -> str:
        """
        获取元素内容
        :param selenium_config:
        :param attribute_type: 常用的值有: id, class, value, innerText
        :return:
        """
        return cls.find(selenium_config).get_attribute(attribute_type)

    @classmethod
    def input(cls, selenium_config: SeleniumConfig, value: str):
        """输入"""
        try:
            assert selenium_config.operate_type == OperateType.action
            element = cls.find(selenium_config)
        except (AssertionError, AttributeError):
            # 参数无法定位
            if value not in Keys.__dict__.values():
                raise ValueError("未指定输入对象时，输入值必须为类Keys。")
            cls.get_action(selenium_config).key_down(value).perform()
        else:
            logging.info("输入元素: %s" % ("*" * len(value) if cls.__check_is_password(element) else value))
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
                if not selenium_config.check_input:
                    break
                # 判断输入结果是否正确
                element_value = element.get_attribute("value")
                if element_value == value:
                    break
                logging.warning(f"元素输入失败，输入的值为: {element_value}")
            else:
                logging.error(f"元素输入失败: {value}\n{traceback.format_exc()}")
                raise RuntimeError("元素输入失败")

    @classmethod
    def select(cls, selenium_config: SeleniumConfig, value: typing.Union[int, str]):
        """选择下拉选项"""
        select = Select(cls.find(selenium_config))  # 实例化Select
        if isinstance(value, int):
            select.select_by_index(value)  # 根据项选择下拉选项
        else:
            try:
                select.select_by_visible_text(value)  # 根据可见文本选择下拉选项
            except common.NoSuchElementException:
                select.select_by_value(value)  # 根据值选择下拉选项

    @classmethod
    def wait_disappear(cls, selenium_config: SeleniumConfig) -> bool:
        """
        等待元素消失
        需要注意的是，检测元素消失的前提是这个元素已经出现
        使用时需要注意，不要在做完上一个操作之后立马调用这个方法，不然可能会出现【要检测消失的元素还未出现，这个方法就已经判断该元素已消失】
        在使用时需要根据具体情况在前面加一定时间的强制等待
        """
        wait_seconds = selenium_config.wait_seconds
        selenium_config.wait_seconds = 1
        time.sleep(1)  # 等待元素加载
        for _ in range(wait_seconds):
            if cls.exist(selenium_config):
                return True
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
    def __get_driver(selenium_config: SeleniumConfig) -> WebDriver:
        """根据参数获取WebDriver"""
        if selenium_config.driver is None:
            selenium_config.driver = ControlBrowser.get_driver(selenium_config)
        return selenium_config.driver

    @classmethod
    def __find(cls, selenium_config: SeleniumConfig, find_method) -> typing.Union[WebElement, typing.List[WebElement]]:
        """显性等待查找元素"""
        if not selenium_config.xpath:
            raise ValueError("查找元素方法必须传入xpath")
        driver = cls.__get_driver(selenium_config) if selenium_config.element is None else selenium_config.element
        # 注！查询间隔为一秒时，这个方法无法检测等待时间为1秒的元素（检测次数为1，即即时检测，而不是预计的等待一秒后报错，因此这里将间隔时间修改为0.3s）
        return WebDriverWait(driver, selenium_config.wait_seconds, 0.3).until(find_method)
