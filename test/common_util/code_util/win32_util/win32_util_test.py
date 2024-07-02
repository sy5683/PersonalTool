from common_core.base.test_base import TestBase
from common_util.code_util.win32_util.win32_util import Win32Util


class Win32UtilTestCase(TestBase):

    def test_find_handle(self):
        handle = Win32Util.find_handle("SunAwtDialog", "附件上传")
        self.assertNotEqual(handle, None)
        print(handle)

    def test_get_root_paths(self):
        root_paths = Win32Util.get_root_paths()
        self.assertNotEqual(root_paths, None)
        print(root_paths)

    def test_press_key(self):
        self.assertEqual(Win32Util.press_key(17, "A"), None)
