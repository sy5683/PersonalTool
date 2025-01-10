from .playwright_utils.control_html.control_element import ControlElement
from .playwright_utils.entity.playwright_config import PlaywrightConfig


class PlaywrightUtil:

    @staticmethod
    def click(playwright_config: PlaywrightConfig):
        """模拟点击"""
        ControlElement.click(playwright_config)
