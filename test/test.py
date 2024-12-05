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
from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.data_util.textual_util.textual_util import TextualUtil
from common_util.file_util.file_util.file_util import FileUtil
from common_util.file_util.image_util.image_util import ImageUtil
from common_util.file_util.json_util.json_util import JsonUtil


class Test(TestBase):

    def setUp(self):
        """"""

    def test_(self):
        """"""
        """
        根据税务验真与勾选场景上线情况，梳理徐爱鹏开发的代码，以新结构重构他和我的脚本代码进行整合。
        查看国税系统中获取发票的界面与相关操作。确认该场景后续开发需求，调研发票池、发票比对相关逻辑。优化税务验真与勾选场景各省份的配置。
        处理用户反馈的问题，收入核对场景优化实现对新格式的增值税申报表与资源税申报表的处理。销项发票分类场景处理软著文件中符号错误的问题。处理纳税申报场景中共享接口无法取到数据的问题。
        查看能投公司月末结账场景新需求文档。并根据新需求对场景进行开发。
        """

    def test_001(self):
        from common_util.code_util.crypto_util.crypto_util import CryptoUtil
        print(CryptoUtil.rsa_encrypt(""))
