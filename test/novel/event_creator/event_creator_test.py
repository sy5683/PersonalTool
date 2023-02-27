import unittest

from personal_tool.novel.event_creator.event_creator import EventCreator


class EventCreatorTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.event_creator = EventCreator()

    def test_main(self):
        self.event_creator.main()

    def test_get_all_roles(self):
        self.event_creator._get_all_roles()
