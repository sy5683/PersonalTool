import time
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
            for index in range(wait_seconds):
                if index:
                    selenium_config.logger = None
                try:
                    cls.find(selenium_config).click()
                except (AttributeError, common.exceptions.ElementNotInteractableException):
                    continue
                break
            else:
                raise common.exceptions.ElementNotInteractableException("点击失败")

    @classmethod
    def exist(cls, selenium_config: SeleniumConfig) -> bool:
        """查找元素是否存在"""
        try:
            element = cls.find(selenium_config)
            assert [element.text] is not None  # 这一行是为了检测入参为WebElement的元素
        except (AssertionError, AttributeError, common.exceptions.ElementNotInteractableException,
                common.exceptions.StaleElementReferenceException):
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
            raise AttributeError("参数中的xpath与element均为空，无法定位元素")
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
        """获取元素内容"""
        return cls.find(selenium_config).get_attribute(attribute_type)

    @classmethod
    def input(cls, selenium_config: SeleniumConfig, value: str):
        """输入"""
        if value in Keys.__dict__.values():
            if selenium_config.operate_type != OperateType.action:
                raise ValueError("输入值为类Keys时，操作方式必须为action。")
            cls.get_action(selenium_config).key_down(value).perform()
        else:
            element = cls.find(selenium_config)
            if element.get_attribute("type") == "password":
                selenium_config.info(f"输入密码: {'*' * len(value)}")
                selenium_config.check_input = False  # 密码无需判断输入结果
            else:
                selenium_config.info(f"输入元素: {value}")
            for _ in range(3):
                if selenium_config.operate_type == OperateType.action:
                    cls._input_element_by_action(selenium_config, element, value)
                else:
                    cls._input_element_by_selenium(element, value)
                # 某些特殊情况无需判断输入结果: 密码、日期格式化、金额会计格式化等
                if not selenium_config.check_input:
                    break
                # 判断输入结果是否正确
                element_value = element.get_attribute("value")
                if element_value == value:
                    break
                selenium_config.info(f"重新输入，元素的值为: {element_value}")
            else:
                raise RuntimeError(f"元素输入失败: {value}")

    @classmethod
    def select(cls, selenium_config: SeleniumConfig, value: typing.Union[int, str]):
        """选择下拉选项"""
        select = Select(cls.find(selenium_config))  # 实例化Select
        if isinstance(value, int):
            select.select_by_index(value)  # 根据项选择下拉选项
        else:
            try:
                select.select_by_visible_text(value)  # 根据可见文本选择下拉选项
            except common.exceptions.NoSuchElementException:
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
        for _ in range(wait_seconds):
            time.sleep(0.2)  # 等待元素加载
            if not cls.exist(selenium_config):
                return True
        return False

    @classmethod
    def _input_element_by_action(cls, selenium_config: SeleniumConfig, element: WebElement, value: str):
        action = cls.get_action(selenium_config)
        # 先将焦点移动到元素上并点击
        action.move_to_element(element).click().perform()
        # 使用action模拟回退按钮删除内容
        element_len = element.get_attribute("value")
        for _ in range(0 if element_len is None else len(element_len)):
            action.send_keys(Keys.RIGHT).perform()
            action.send_keys(Keys.BACK_SPACE).perform()
            time.sleep(0.1)
        # 模拟全选
        action.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        # 输入元素
        action.send_keys(value).perform()

    @staticmethod
    def _input_element_by_selenium(element: WebElement, value: str):
        # 先点击定位
        try:
            element.click()
        except (common.exceptions.ElementClickInterceptedException, common.exceptions.ElementNotInteractableException):
            pass  # 元素可能无法点击
        time.sleep(0.2)
        # 使用selenium自带的clear方法清空元素
        try:
            element.clear()
        except common.exceptions.InvalidElementStateException:
            pass  # 元素可能无法清空
        time.sleep(0.2)
        # 有时候有输入框 element.clear() 方法无效，因此再使用手动按键方式清空一次
        for _ in range(len(element.get_attribute("value"))):
            element.send_keys(Keys.RIGHT)
            element.send_keys(Keys.BACK_SPACE)
            time.sleep(0.1)
        # 模拟全选
        element.send_keys(Keys.CONTROL, "a")
        time.sleep(0.2)
        # 输入元素
        element.send_keys(value)

    @classmethod
    def __find(cls, selenium_config: SeleniumConfig, find_method) -> typing.Union[WebElement, typing.List[WebElement]]:
        """显性等待查找元素"""
        if not selenium_config.xpath:
            raise ValueError("查找元素方法必须传入xpath")
        time.sleep(selenium_config.delay_seconds)
        driver = cls.__get_driver(selenium_config) if selenium_config.element is None else selenium_config.element
        # 注！查询间隔为一秒时，这个方法无法检测等待时间为1秒的元素（检测次数为1，即即时检测，而不是预计的等待一秒后报错，因此这里将间隔时间修改为0.3s）
        try:
            return WebDriverWait(driver, selenium_config.wait_seconds, 0.3).until(find_method)
        except (common.exceptions.NoSuchElementException, common.exceptions.TimeoutException):
            raise AttributeError(f"未找到指定元素: {selenium_config.xpath}")

    @staticmethod
    def __get_driver(selenium_config: SeleniumConfig) -> WebDriver:
        """根据参数获取WebDriver"""
        if selenium_config.driver is None:
            selenium_config.driver = ControlBrowser.get_driver(selenium_config)
        return selenium_config.driver
