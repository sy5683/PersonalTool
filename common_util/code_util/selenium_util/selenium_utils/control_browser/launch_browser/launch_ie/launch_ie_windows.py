import threading

import win32con
from selenium.webdriver.ie.webdriver import WebDriver
from win32api import RegCloseKey, RegOpenKey, RegSetValueEx

from .launch_ie import LaunchIe
from ....entity.selenium_config import SeleniumConfig


class LaunchIeWindows(LaunchIe):

    @classmethod
    def get_driver(cls, selenium_config: SeleniumConfig) -> WebDriver:
        """获取driver"""
        # 1) 返回参数中传入的driver
        if selenium_config.driver:
            return selenium_config.driver
        # 2) 启动IE浏览器需要初始化其对应的参数与缩放比例
        cls._set_ie_setting()
        # 3) 获取进程id，并启动IE浏览器
        thread_id = threading.current_thread().ident
        if thread_id not in cls._driver_map:
            cls._driver_map[thread_id] = cls._launch_ie(selenium_config)
        return cls._driver_map[thread_id]

    @classmethod
    def _set_ie_setting(cls):
        """设置IE浏览器，这些设置是selenium启动IE浏览器的必要条件"""

        def set_regedit_value(regedit_path: str, regedit_key: str, regedit_value: int):
            key = RegOpenKey(win32con.HKEY_CURRENT_USER, regedit_path, 0, win32con.KEY_ALL_ACCESS)
            RegSetValueEx(key, regedit_key, 0, win32con.REG_DWORD, regedit_value)
            RegCloseKey(key)

        # 1) 设置浏览器缩放为100%
        set_regedit_value("Software/Microsoft/Internet Explorer/Zoom", "ZoomFactor", 100000)
        # 2) 设置浏览器所有保护模式统一开启或关闭
        for each in range(1, 5):
            # 最后一个参数: 0->开启, 3->关闭
            set_regedit_value(f"Software/Microsoft/Windows/CurrentVersion/Internet Settings/Zones/{each}", "2500",
                              3)
