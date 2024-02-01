from common_core.base.test_base import TestBase
from common_util.visual_util.dialog_util.dialog_util import DialogUtil


class DialogUtilTestCase(TestBase):

    def test_message_box(self):
        self.assertEqual(DialogUtil.message_box("测试弹窗"), None)
