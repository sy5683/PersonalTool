import unittest

from personal_tool.novel.event_creator.feture.entity_feature import EntityFeature


class EntityFeatureTestCase(unittest.TestCase):

    def test_get_all_roles(self):
        all_roles = EntityFeature.get_all_roles()
        self.assertNotEqual(all_roles, None)
        for role in all_roles:
            print(role.__dict__)
