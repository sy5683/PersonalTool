import logging
import re
import typing
from pathlib import Path

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from .base.crawler_base import CrawlerBase


class Crawler001(CrawlerBase):

    def __init__(self, save_path: typing.Union[Path, str]):
        super().__init__("抖音小说", save_path)

    def run(self, **kwargs):
        url_suffix = kwargs['url_suffix']
        SeleniumUtil.open_url(f"https://www.douyinxs.com/{url_suffix.strip('/')}")
        with open(self.save_path, "w+") as file:
            # file.truncate()  # 清空
            while True:
                try:
                    next_button = SeleniumUtil.find('//a[@id="next"]')
                except Exception as e:
                    logging.warning(f"页面异常，重新刷新: {e}")
                    SeleniumUtil.get_driver().refresh()
                if "下一页" in next_button.get_attribute("innerText"):
                    title = SeleniumUtil.find('//div[@class="bookname"]/h1').get_attribute("innerText")
                    file.write(f"\n\n{title}\n")
                    print(title)
                content_element = SeleniumUtil.find('//article[@id="content"]').get_attribute("innerText")
                for each in re.split(r"\s+", content_element):
                    if not each:
                        continue
                    file.write(f"        {each}\n")
                if "书末页" in next_button.get_attribute("innerText"):
                    break
                next_button.click()
