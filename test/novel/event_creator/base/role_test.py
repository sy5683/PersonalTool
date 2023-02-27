import unittest

from personal_tool.novel.event_creator.base.role import Role


class RoleTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.role = Role()
