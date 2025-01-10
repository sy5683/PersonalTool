import typing

from .launch_browser.base.launch_base import LaunchBase
from .launch_browser.launch_chrome import LaunchChrome
from ..enum.browser_type import BrowserType


class ControlBrowser:

    @staticmethod
    def _get_launch_class(browser_type: BrowserType) -> typing.Type[LaunchBase]:
        if browser_type == BrowserType.chrome:
            return LaunchChrome
        else:
            raise TypeError(f"暂不支持的浏览器类型: {browser_type.name}")
