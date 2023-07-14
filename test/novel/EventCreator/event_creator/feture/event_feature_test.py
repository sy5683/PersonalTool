import unittest

from personal_tool.novel.EventCreator.event_creator.feture.event_feature import EventFeature


class EventFeatureTestCase(unittest.TestCase):

    def test_get_all_events(self):
        all_events = EventFeature.get_all_events()
        self.assertNotEqual(all_events, None)
        for event in all_events:
            print(event)

    def test_get_undone_event(self):
        undone_event = EventFeature.get_undone_event()
        self.assertNotEqual(undone_event, None)
        print(undone_event)
