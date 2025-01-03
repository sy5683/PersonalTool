import base64
import collections
import json
import logging
import os
import random
import re
import tempfile
import time
import typing
import unittest
import winreg
from pathlib import Path

import cv2
import numpy
import openpyxl
import win32api
from PIL import Image
from bs4 import BeautifulSoup
from selenium import common
from selenium.webdriver import ActionChains, Keys
from webdriver_manager.chrome import ChromeDriverManager

from common_core.base.test_base import TestBase
from common_util.code_util.net_util.net_util import NetUtil
from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig
from common_util.code_util.selenium_util.selenium_utils.enum.operate_type import OperateType
from common_util.code_util.win32_util.win32_util import Win32Util
from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.data_util.textual_util.textual_util import TextualUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from common_util.file_util.file_util.file_util import FileUtil
from common_util.file_util.image_util.image_util import ImageUtil
from common_util.file_util.json_util.json_util import JsonUtil


class Test(TestBase):

    def setUp(self):
        """"""

    def test_(self):
        """"""

    def test_001(self):
        """密码加密"""
        from common_util.code_util.crypto_util.crypto_util import CryptoUtil
        print(CryptoUtil.rsa_encrypt(""))

    def test_002(self):
        """自动推送"""
        time.sleep(1)
        while True:
            logging.info("开始推送")
            Win32Util.press_key("ctrl", "shift", "k")
            time.sleep(0.5)
            Win32Util.press_key("alt", "p")
            time.sleep(23)  # 连接超时平均是在21000ms到22000ms之间