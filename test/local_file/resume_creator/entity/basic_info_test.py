import unittest

from personal_tool.local_file.resume_creator.entity.info.basic_info import BasicInfo


class BasicInfoTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_info = BasicInfo()

    def test_show(self):
        for key, value in self.basic_info.__dict__.items():
            print(key, value)
