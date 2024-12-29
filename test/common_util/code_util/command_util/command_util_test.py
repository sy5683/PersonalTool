from common_core.base.test_base import TestBase
from common_util.code_util.command_util.command_util import CommandUtil


class CommandUtilTestCase(TestBase):

    def test_check_process_running(self):
        result = CommandUtil.check_process_running("pycharm64.exe")
        self.assertNotEqual(result, None)
        print(result)

    def test_install_python_package(self):
        self.assertEqual(CommandUtil.install_python_package("onnxruntime"), None)

    def test_install_python_packages(self):
        packages_str = """"""
        for package in packages_str.split("\n"):
            package, version = (package.split("==") + [""])[:2]
            self.assertEqual(CommandUtil.install_python_package(package, version), None)
