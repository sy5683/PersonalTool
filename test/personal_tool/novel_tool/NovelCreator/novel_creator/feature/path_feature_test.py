import unittest

from personal_tool.novel_tool.NovelCreator.novel_creator.feature.path_feature import PathFeature


class PathFeatureTestCase(unittest.TestCase):

    def test_to_novel_path(self):
        novel_path = PathFeature.to_novel_path("构灵")
        self.assertNotEqual(novel_path, None)
        print(novel_path)
