from common_core.base.test_base import TestBase
from common_util.data_util.textual_util.textual_util import TextualUtil


class TextualUtilTestCase(TestBase):

    def setUp(self):
        # self.textual = "\u738A\u70E8"
        self.textual = "\\u738A\\u70E8"
        # self.textual = "\xe7\x8e\x8a\xe7\x83\xa8"
        # self.textual = b"\\xe7\\x8e\\x8a\\xe7\\x83\\xa8"

    def test_textual_decode(self):
        result_textual = TextualUtil.textual_decode(self.textual)
        print(result_textual)
