import abc
import os
import threading
import time
import typing

from selenium import webdriver, common
from selenium.webdriver.edge.webdriver import WebDriver

from ..base.launch_base import LaunchBase
from ..download_driver import DownloadDriver
from ....entity.selenium_config import SeleniumConfig


class LaunchEdge(LaunchBase):
    _driver_map: typing.Dict[int, WebDriver] = {}

    @classmethod
    def close_browser(cls, selenium_config: SeleniumConfig):
        """关闭Edge浏览器"""
        # 1) 确认参数、缓存中的driver是否存在，不存在则返回
        driver = selenium_config.driver
        if driver is None:
            driver = cls._driver_map.get(threading.current_thread().ident)
        if driver is None:
            return
        # 2) 使用selenium自带的quit方法关闭driver
        driver.quit()
        time.sleep(1)  # 等待一秒，确认等待操作执行完成
        # 3) 清除缓存
        selenium_config.driver = None
        for key, _driver in list(cls._driver_map.items()):
            if driver == _driver:
                del cls._driver_map[key]

    @classmethod
    @abc.abstractmethod
    def get_driver(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """获取driver"""
        return cls.__get_subclass().get_driver(selenium_config)

    @classmethod
    def _get_edge_driver(cls, selenium_config: SeleniumConfig, user_data_dir: str = None) -> WebDriver:
        """获取edge_driver"""
        # 1.1) 获取Edge浏览器设置
        options = webdriver.EdgeOptions()
        # 1.2.1) 设置静默运行
        if selenium_config.headless:
            options.add_argument('--headless')
        # 1.2.2) 设置ip代理
        if selenium_config.proxy_ip:
            options.add_argument(f"--proxy-server={selenium_config.proxy_ip}")
        # 1.3.1) 设置忽略私密链接警告
        options.add_argument('--ignore-certificate-errors')
        # 1.3.2) 设置取消提示受自动控制
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        # 1.4.1) 伪装浏览器请求头
        options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
        # 1.4.2) 去掉webdriver痕迹
        options.add_argument("disable-blink-features=AutomationControlled")
        # 1.5) 取消提示和默认下载路径在同一个参数中配置
        prefs = options.experimental_options.get("prefs", {})
        # 1.5.1) 设置取消提示
        prefs.update({'credentials_enable_service': False})  # 设置取消提示保存密码
        prefs.update({'download.prompt_for_download': False})  # 取消提示下载
        # 1.5.2) 设置默认下载路径
        selenium_config.info(f"浏览器下载路径为: {selenium_config.download_path}")
        if os.path.exists(selenium_config.download_path):
            prefs.update({'download.default_directory': selenium_config.download_path})
        options.add_experimental_option('prefs', prefs)
        # 1.6) 设置读取用户缓存目录
        if user_data_dir and os.path.exists(user_data_dir):
            options.add_argument(f"--user-data-dir={user_data_dir}")
        # 2) 启动Edge浏览器
        return cls.__launch_edge_driver(selenium_config, options)

    @classmethod
    @abc.abstractmethod
    def _get_edge_path(cls) -> str:
        """获取Edge浏览器路径"""
        return cls.__get_subclass()._get_edge_path()

    @classmethod
    def _launch_edge(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """启动Edge浏览器"""
        selenium_config.info("启动Edge浏览器")
        try:
            assert selenium_config.use_user_data
            # 1.1) 获取Edge浏览器用户缓存路径
            user_data_dir = cls.__get_user_data_path()
            # 1.2) 获取driver
            driver = cls._get_edge_driver(selenium_config, user_data_dir)
        except (AssertionError, common.exceptions.InvalidArgumentException,
                common.exceptions.SessionNotCreatedException):
            # 1.3) 重新获取driver，不加载user_data_dir
            driver = cls._get_edge_driver(selenium_config)
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(selenium_config.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        return driver

    @classmethod
    def _launch_edge_with_ie(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """ie模式启动Edge浏览器"""
        selenium_config.info("ie模式启动Edge浏览器")
        from ..launch_ie.launch_ie import LaunchIe
        # 1.1) 获取IE浏览器设置
        options = webdriver.IeOptions()
        # 1.2.1) IE浏览器无法设置静默运行
        # 1.2.2) 设置ip代理
        if selenium_config.proxy_ip:
            options.add_argument(f"--proxy-server={selenium_config.proxy_ip}")
        # 1.3) 使用edge启动
        options.attach_to_edge_chrome = True
        options.edge_executable_path = cls._get_edge_path()
        # 2) 启动IE浏览器
        driver = LaunchIe._launch_ie_driver(selenium_config, options)
        # 3.1) 设置默认加载超时时间
        driver.set_page_load_timeout(selenium_config.wait_seconds)
        # 3.2) 启动后设置浏览器最前端
        cls.set_browser_front(driver)
        return driver

    @staticmethod
    def __get_driver_path(selenium_config: SeleniumConfig) -> str:
        """获取driver路径"""
        # 1) 使用参数中的driver_path
        if selenium_config.driver_path:
            return selenium_config.driver_path
        # 2) 自动获取下载的driver_path路径
        return DownloadDriver.get_edge_driver_path()

    @staticmethod
    def __get_user_data_path() -> typing.Union[str, None]:
        """获取Edge浏览器用户缓存User Data路径"""
        # 1) 查找User Data文件默认路径
        user_data_path = os.path.join(os.path.expanduser('~'), "AppData", "Local", "Microsoft", "Edge", "User Data",
                                      "Default")
        if os.path.exists(user_data_path):
            return user_data_path
        # 2) 返回空值
        return None

    @classmethod
    def __launch_edge_driver(cls, selenium_config: SeleniumConfig, options: webdriver.EdgeOptions) -> WebDriver:
        """启动Edge浏览器driver"""
        driver_path = cls.__get_driver_path(selenium_config)
        from selenium.webdriver.edge.service import Service
        return webdriver.Edge(options=options, service=Service(executable_path=driver_path))

    @staticmethod
    def __get_subclass():
        if os.name == "nt":
            from .launch_edge_windows import LaunchEdgeWindows
            return LaunchEdgeWindows
        elif os.name == "posix":
            from .launch_edge_linux import LaunchEdgeLinux
            return LaunchEdgeLinux
        raise Exception(f"未知的操作系统类型: {os.name}")
