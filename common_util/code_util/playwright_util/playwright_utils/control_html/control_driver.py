import time

from ..control_browser.control_browser import ControlBrowser
from ..entity.playwright_config import PlaywrightConfig


class ControlDriver:

    @staticmethod
    def open_url(playwright_config: PlaywrightConfig, url: str):
        """打开url"""
        for _ in range(3):
            try:
                browser, context, page = ControlBrowser.get_driver(playwright_config)
                page.goto(url)
                break
            except OSError:  # selenium驱动升级会导致driver失效，会报错OSError
                playwright_config.info("selenium启动异常，重新启动")
                time.sleep(1)

    @staticmethod
    def refresh(playwright_config: PlaywrightConfig):
        """刷新"""
        browser, context, page = ControlBrowser.get_driver(playwright_config)
        page.reload()
