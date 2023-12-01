import unittest
from pathlib import Path

from common_util.code_util.import_util.import_util import ImportUtil


class ImportUtilTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.module_path = Path(__file__)

    def test_import_module(self):
        module = ImportUtil.import_module(self.module_path)
        print(module)
