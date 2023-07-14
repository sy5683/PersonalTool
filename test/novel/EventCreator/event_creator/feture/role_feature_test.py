import unittest

from personal_tool.novel.EventCreator.event_creator.feture.role_feature import RoleFeature


class RoleFeatureTestCase(unittest.TestCase):

    def test_get_all_roles(self):
        all_roles = RoleFeature.get_all_roles()
        self.assertNotEqual(all_roles, None)
        for role in all_roles:
            print(role)

    def test_get_random_roles(self):
        random_roles = RoleFeature.get_random_roles()
        self.assertNotEqual(random_roles, None)
        for role in random_roles:
            print(role)
