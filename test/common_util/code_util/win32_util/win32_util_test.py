import unittest

from common_util.code_util.win32_util.win32_util import Win32Util


class Win32UtilTestCase(unittest.TestCase):

    def test_find_handle(self):
        handle = Win32Util.find_handle("SunAwtDialog", "附件上传")
        self.assertNotEqual(handle, None)
        print(handle)
