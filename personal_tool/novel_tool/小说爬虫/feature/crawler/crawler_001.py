import logging
import re
import typing
from pathlib import Path

from selenium import common

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from .base.crawler_base import CrawlerBase


class Crawler001(CrawlerBase):

    def __init__(self, save_path: typing.Union[Path, str]):
        super().__init__("抖音小说", save_path)

    def run(self, **kwargs):
        url_suffix = kwargs['url_suffix']
        SeleniumUtil.open_url(f"https://www.douyinxs.com/{url_suffix.strip('/')}")
        driver = SeleniumUtil.get_driver()
        driver.set_page_load_timeout(10)
        with open(self.save_path, "w+", encoding='UTF-8') as file:
            temp_contents = []
            while True:
                while True:
                    try:
                        element = SeleniumUtil.find('//article[@id="content"]', without_log=True)
                        contents = [each for each in re.split(r"\n", element.get_attribute("innerText")) if each]
                        if contents != temp_contents:
                            temp_contents = contents
                            break
                    except Exception as e:
                        logging.warning(e)
                next_button = SeleniumUtil.find('//a[@id="next"]')
                if "下一页" in next_button.get_attribute("innerText"):
                    title = SeleniumUtil.find('//div[@class="bookname"]/h1').get_attribute("innerText")
                    file.write(f"\n\n{title}\n")
                    print(title)
                for content in contents:
                    file.write(f"　　{content}\n")
                if "书末页" in next_button.get_attribute("innerText"):
                    break
                # 点击下一页或者下一章时，可能因为频率太快导致页面无法加载，会在这里报错，因此在这里捕捉一下并刷新一下即可
                while True:
                    try:
                        next_button.click()
                    except common.TimeoutException:
                        while True:
                            try:
                                driver.refresh()  # 刷新可能也会有问题
                            except common.TimeoutException:
                                pass
                            break
                    break
