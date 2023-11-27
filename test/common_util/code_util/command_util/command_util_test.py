import unittest

from common_util.code_util.command_util.command_util import CommandUtil


class CommandUtilTestCase(unittest.TestCase):

    def test_check_process_running(self):
        result = CommandUtil.check_process_running("pycharm64.exe")
        self.assertNotEqual(result, None)
        print(result)

    def test_pip_install(self):
        self.assertEqual(CommandUtil.pip_install(""), None)
