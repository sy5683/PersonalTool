import re

from playwright.sync_api import *

from ..control_browser.control_browser import ControlBrowser
from ..control_browser.launch_browser.launch_chrome import LaunchChrome
from ..entity.playwright_config import PlaywrightConfig


class ControlWindow:

    @classmethod
    def close_other_window(cls, playwright_config: PlaywrightConfig, *window_titles: str):
        """关闭其他窗口"""
        _, context, _ = ControlBrowser.get_driver(playwright_config)
        for page in context.pages:
            title = page.title()
            for window_title in window_titles:
                if window_title and re.search(window_title, title):
                    break
                elif not window_title and window_title == title:
                    break
            else:
                # 需要注意，为了保证浏览器活性，当最后一个窗口仍不满足条件时，需要保留窗口
                if len(context.pages) == 1:
                    raise RuntimeWarning(f"指定窗口不存在，将所有窗口关闭，保留一个窗口: {page.title()}")
                playwright_config.info(f"关闭窗口: {title}")
                page.close()
        # 关闭完窗口之后还需要重新切换一下窗口
        cls.switch_window(playwright_config, window_titles[-1])

    @classmethod
    def switch_window(cls, playwright_config: PlaywrightConfig, window_title: str):
        """切换窗口"""
        _, context, _ = ControlBrowser.get_driver(playwright_config)
        for _ in range(max((playwright_config.wait_seconds // len(context.pages)), 1)):
            target_pages = []
            for page in context.pages:
                # 校验标题
                title = page.title()
                if window_title and not re.search(window_title, title):
                    continue
                elif not window_title and window_title != title:
                    continue
                target_pages.append(page)
            # 根据提取到的窗口情况进行处理
            if len(target_pages) == 1:
                page = target_pages[0]
                playwright_config.info(f"切换到窗口: {page.title if window_title else window_title}")
                cls._switch_page(playwright_config, page)
                break
            elif not target_pages:
                playwright_config.info("指定的窗口数量为空，重新查询")
            else:
                cls._switch_page(playwright_config, target_pages[-1])
                raise IndexError(f"出现多个包含【{window_title}】的目标窗口")
        else:
            cls._switch_page(playwright_config, context.pages[-1])  # 切换至最新窗口
            raise IndexError(f"未找到目标窗口: {window_title}")

    @staticmethod
    def _switch_page(playwright_config: PlaywrightConfig, page: Page):
        """切换至指定页签"""
        # 激活当前窗口
        page.bring_to_front()
        # 切换完成需要将缓存中的焦点句柄替换掉，否则其余方法定位时会出错
        LaunchChrome.update_driver(playwright_config, page=page)
