import xml

import xmltodict

from common_core.base.test_base import TestBase
from common_util.data_util.textual_util.textual_util import TextualUtil


class TextualUtilTestCase(TestBase):

    def setUp(self):
        # self.textual = "\u738A\u70E8"
        self.textual = "\\u738A\\u70E8"
        # self.textual = "\xe7\x8e\x8a\xe7\x83\xa8"
        # self.textual = b"\\xe7\\x8e\\x8a\\xe7\\x83\\xa8"
        self.response_string = """"""

    def test_extract_tax_rate(self):
        self.textual = "应交税费-应交增值税-进项税额-一般进项税-税率13%"
        tax_rate = TextualUtil.extract_tax_rate(self.textual)
        print(tax_rate)

    def test_textual_decode(self):
        result_textual = TextualUtil.textual_decode(self.textual)
        print(result_textual)

    def test_check_error(self):
        split_key = "INFO"
        split_strings = self.response_string.split(f"</{split_key}><{split_key}>")
        for index, response_string in enumerate(split_strings):
            if index != 0:
                response_string = f"<{split_key}>{response_string}"
            if index != len(split_strings) - 1:
                response_string = f"{response_string}</{split_key}>"
            result_string = TextualUtil.textual_decode(response_string)
            try:
                xmltodict.parse(result_string)
            except xml.parsers.expat.ExpatError:
                print(f"【{index}】\n{result_string}")
