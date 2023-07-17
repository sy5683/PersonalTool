import unittest

from personal_tool.game.GameCode.game_code.feature.file_feature import FileFeature


class FileFeatureTestCase(unittest.TestCase):

    def test_to_database_path(self):
        database_path = FileFeature.to_database_path()
        self.assertNotEqual(database_path, None)
        print(database_path)
