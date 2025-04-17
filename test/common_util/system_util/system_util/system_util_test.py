from common_core.base.test_base import TestBase
from common_util.system_util.system_util.system_util import SystemUtil
from common_util.system_util.system_util.system_utils.enum.system_type import SystemType


class SystemUtilTestCase(TestBase):

    def test_get_system_type(self):
        system_type = SystemUtil.get_system_type()
        self.assertNotEqual(system_type, SystemType.unknown)
        print(system_type)
