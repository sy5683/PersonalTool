import unittest

from personal_tool.local_file.FileFormat.file_format.feature.file_feature import FileFeature


class FileFeatureTestCase(unittest.TestCase):

    def test_get_directory_path(self):
        directory_path = FileFeature.get_directory_path()
        self.assertNotEqual(directory_path, None)
        print(directory_path)
        print(type(directory_path))
