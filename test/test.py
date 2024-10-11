import collections
import json
import os
import random
import re
import tempfile
import time
import typing
import unittest
from pathlib import Path

import cv2
import openpyxl
import win32api
from PIL import Image
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains, Keys
from webdriver_manager.chrome import ChromeDriverManager

from common_core.base.test_base import TestBase
from common_util.code_util.net_util.net_util import NetUtil
from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig
from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.data_util.textual_util.textual_util import TextualUtil
from common_util.file_util.image_util.image_util import ImageUtil
from common_util.file_util.json_util.json_util import JsonUtil


class Test(TestBase):

    def setUp(self):
        """"""

    def test_(self):
        """"""
