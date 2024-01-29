from common_core.base.test_base import TestBase
from common_util.code_util.import_util.import_util import ImportUtil


class ImportUtilTestCase(TestBase):

    def setUp(self) -> None:
        self.module_path = self.get_test_file()

    def test_import_module(self):
        module = ImportUtil.import_module(self.module_path)
        print(module)
