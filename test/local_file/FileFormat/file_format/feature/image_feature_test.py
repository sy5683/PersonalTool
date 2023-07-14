import unittest

from personal_tool.local_file.FileFormat.file_format.feature.image_feature import ImageFeature


class ImageFeatureTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.image_path = ""

    def test_convert_webp_to_jpg(self):
        ImageFeature.convert_webp_to_jpg(self.image_path)
