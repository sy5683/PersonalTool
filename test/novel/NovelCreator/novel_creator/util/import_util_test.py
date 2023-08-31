import unittest

from personal_tool.novel.NovelCreator.novel_creator.feature.entity.event import Event
from personal_tool.novel.NovelCreator.novel_creator.feature.path_feature import PathFeature
from personal_tool.novel.NovelCreator.novel_creator.util.import_util import ImportUtil


class ImportUtilTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.module_path = PathFeature.to_novel_path("构灵")

    def test_import_module(self):
        module = ImportUtil.import_module(self.module_path)
        print(module)

    def test_import_modules(self):
        ImportUtil.import_modules(self.module_path)
        for event in Event.__subclasses__():
            print(event)
