import os
import re
import typing

from selenium.common import TimeoutException

from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from .file_feature import FileFeature


class TitleFeature:

    @classmethod
    def craw_titles(cls, url: str = None):
        """爬取标题"""
        if url:
            SeleniumUtil.open_url(url)
        with open(cls.__get_titles_path(), "w+", encoding='utf-8') as file:
            file.truncate()
            while True:
                for title_element in SeleniumUtil.finds('//div[@id="list"]/dl/dd')[12:]:
                    file.write(f'{title_element.get_attribute("innerText")}\n')
                try:
                    SeleniumUtil.click('//a[text()="下一页"]', wait_seconds=3)
                except TimeoutException:
                    break

    @classmethod
    def replace_titles(cls, novel_path: str):
        assert novel_path, "未选择小说"
        # 读取原小说内容
        with open(novel_path, "r", encoding='utf-8') as file:
            contexts = file.readlines()
        # 获取爬取的标题
        with open(cls.__get_titles_path(), "r", encoding='utf-8') as file:
            titles = [re.sub("章[:：]", "章 ", each) for each in file.readlines()]
        # 替换标题
        _novel_name, _suffix = os.path.splitext(novel_path)
        with open(f"{_novel_name}_new{_suffix}", "w+", encoding='utf-8') as file:
            for context in contexts:
                chapter_number = re.search(r"^第(.*?)章", context)
                if chapter_number:
                    for title in titles:
                        if chapter_number.group(0) in title:
                            context = title
                            break
                file.write(context)

    @classmethod
    def get_titles(cls) -> typing.List[str]:
        """获取标题"""

    @staticmethod
    def __get_titles_path() -> str:
        """获取标题文件路径"""
        return FileFeature.get_file_path("title.txt")
