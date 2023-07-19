import re
import unittest

import fitz


class Test(unittest.TestCase):

    def test_(self):
        """"""
        image_path = r"E:\Download\VOneManagerMan.exe"
        fitz.open(image_path)
