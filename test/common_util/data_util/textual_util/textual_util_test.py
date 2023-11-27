import unittest

from common_util.data_util.textual_util.textual_util import TextualUtil


class TextualUtilTestCase(unittest.TestCase):

    def setUp(self):
        self.textual = "\\u738A\\u70E8"

    def test_textual_decode(self):
        result_textual = TextualUtil.textual_decode(self.textual)
        print(result_textual)
