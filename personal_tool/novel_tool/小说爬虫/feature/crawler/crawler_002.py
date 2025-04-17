import logging
import re
import typing

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig
from .base.crawler_base import CrawlerBase


class Crawler002(CrawlerBase):

    def __init__(self, save_path: typing.Union[pathlib.Path, str]):
        super().__init__("95书包", save_path)

    def run(self, **kwargs):
        url_suffix = kwargs['url_suffix']
        SeleniumUtil.open_url(SeleniumConfig(), f"http://www.95dushu.net/{url_suffix.strip('/')}")
        driver = SeleniumUtil.get_driver(SeleniumConfig())
        driver.set_page_load_timeout(10)
        with open(self.save_path, "w+", encoding='UTF-8') as file:
            temp_contents = []
            while True:
                if not re.search("\.html$", driver.current_url):
                    break
                while True:
                    try:
                        element = SeleniumUtil.find(SeleniumConfig(xpath='//div[@id="content"]', logger=None))
                        contents = [each for each in re.split(r"\n", element.get_attribute("innerText")) if each]
                        if contents != temp_contents:
                            temp_contents = contents
                            break
                    except Exception as e:
                        logging.warning(e)
                title = SeleniumUtil.get_attribute(SeleniumConfig(xpath='//div[@class="info"]/h1'), "innerText")
                title = title.replace("正文卷 ", "")
                file.write(f"\n\n{title}\n")
                for content in contents:
                    if content == "最新网址：www.95dushu.net":
                        continue
                    content = content.strip()
                    file.write(f"    {content}\n")
                SeleniumUtil.click(SeleniumConfig(xpath='//a[text()="下一章"]'))
                # 点击下一章时，可能因为频率太快导致导致503报错，因此在这里捕捉一下并刷新一下即可
                while True:
                    try:
                        assert not SeleniumUtil.wait_disappear(
                            SeleniumConfig(xpath='//center/h1[contains(text(), "503")]', wait_seconds=1))
                        break
                    except AssertionError:
                        driver.refresh()
