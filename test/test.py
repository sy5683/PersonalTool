import os
import re
import tempfile
import time
import unittest
from pathlib import Path

import openpyxl
import win32api
from selenium.webdriver import ActionChains, Keys

from common_core.base.test_base import TestBase
from common_util.code_util.net_util.net_util import NetUtil
from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.selenium_util.selenium_utils.selenium_config import SeleniumConfig


class Test(TestBase):

    def setUp(self):
        """"""

    def test_(self):
        """"""

    def test_001(self):
        workbook = openpyxl.Workbook()
        # SeleniumUtil.open_url("https://ec.chng.com.cn/channel/home/?SlJfApAfmEBp=1710987207840#/purchase?checked=3")
        content = SeleniumUtil.finds('//div[@class="content"]')[0]
        next_element = SeleniumUtil.find('.//li[@title="下一页"]', driver=content)
        for tag in SeleniumUtil.finds('./div[@class="menu"]/div', driver=content):
            SeleniumUtil.click(tag)
            tag_name = tag.get_attribute("innerText")
            worksheet = workbook.create_sheet(tag_name)
            worksheet.append(["标题", "时间"])
            for index in range(50):
                if index:
                    SeleniumUtil.click(next_element)
                time.sleep(1)
                table = SeleniumUtil.find('.//tbody[@class="ant-table-tbody"]', driver=content)
                for element in SeleniumUtil.finds('./tr', driver=table):
                    title = SeleniumUtil.find('.//span[@class="list-text"]', driver=element).get_attribute("innerText")
                    datetime = SeleniumUtil.find('.//p', driver=element).get_attribute("innerText")
                    worksheet.append([title, datetime])
        workbook.remove(workbook['Sheet'])
        workbook.save("test.xlsx")
        workbook.close()
