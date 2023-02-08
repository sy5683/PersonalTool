import unittest

from personal_tool.fallout.fallout_4_code.fallout_4_code import Fallout4Code


class Fallout4CodeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.fallout_4_code = Fallout4Code()

    def test_main(self):
        self.fallout_4_code.main()

    def test_add_item(self):
        self.fallout_4_code.add_item()

    def test_get_item_command(self):
        self.fallout_4_code.get_item_command()
        self.fallout_4_code.sqlite_connect.close()

    def test_show_items(self):
        self.fallout_4_code.show_items()
        self.fallout_4_code.sqlite_connect.close()

    def test_get_command(self):
        item_code = ""
        command = self.fallout_4_code._get_command(item_code)
        print(command)

    def tearDown(self) -> None:
        self.fallout_4_code.sqlite_connect.close()
