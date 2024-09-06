import json
import os
import random
import re
import tempfile
import time
import unittest
from pathlib import Path

import cv2
import openpyxl
import win32api
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains, Keys
from webdriver_manager.chrome import ChromeDriverManager

from common_core.base.test_base import TestBase
from common_util.code_util.net_util.net_util import NetUtil
from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.data_util.textual_util.textual_util import TextualUtil
from common_util.file_util.image_util.image_util import ImageUtil


class Test(TestBase):

    def setUp(self):
        """"""

    def test_(self):
        """"""
        from common_util.code_util.temp_util.selenium_util import SeleniumUtil
        from common_util.code_util.temp_util.selenium_utils.entity.selenium_config import SeleniumConfig

        driver_path = SeleniumUtil.get_chrome_driver_path()
        SeleniumUtil.open_url(SeleniumConfig(driver_path=driver_path), "https://www.baidu.com/")  # 打开url
        element = SeleniumUtil.find(SeleniumConfig(xpath='//map[@id="s_mp"]/area', wait_seconds=30))  # 查找元素
        SeleniumUtil.find(SeleniumConfig(xpath='./ancestor::div[@id="lg"]', element=element))  # 查找父级元素
