from common_core.base.test_base import TestBase
from common_util.code_util.win32_util.win32_util import Win32Util


class Win32UtilTestCase(TestBase):

    def test_find_handle(self):
        handle = Win32Util.find_handle("SunAwtDialog", "附件上传")
        self.assertNotEqual(handle, None)
        print(handle)

    def test_input(self):
        self.assertEqual(Win32Util.input("123456"), None)

    def test_press_key(self):
        self.assertEqual(Win32Util.press_key("ctrl", "a"), None)
