import unittest

from personal_tool.local_file.gif_creator.gif_creator import GifCreator


class GifCreatorTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.gif_creator = GifCreator()

    def test_main(self):
        self.gif_creator.main()
