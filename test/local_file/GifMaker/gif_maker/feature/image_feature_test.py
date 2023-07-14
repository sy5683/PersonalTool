import unittest

from personal_tool.local_file.GifMaker.gif_maker.feature.image_feature import ImageFeature


class ImageFeatureTestCase(unittest.TestCase):

    def test_get_image_paths(self):
        image_paths = ImageFeature.get_image_paths()
        self.assertNotEqual(image_paths, None)
        for image_path in image_paths:
            print(image_path)
