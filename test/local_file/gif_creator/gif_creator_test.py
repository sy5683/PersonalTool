import unittest

from personal_tool.local_file.gif_creator.gif_creator import GifCreator, CreatorMode


class GifCreatorTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.gif_creator = GifCreator(CreatorMode.rotate)

    def test_main(self):
        self.gif_creator.main()
