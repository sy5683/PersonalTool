import unittest

from personal_tool.novel.PersonNameCreator.person_name_creator.feature.surname.surname_feature import SurnameFeature


class SurnameFeatureTestCase(unittest.TestCase):

    def test_get_surname(self):
        surname = SurnameFeature.get_surname("玊")
        self.assertNotEqual(surname, None)
        print(surname)

    def test_get_surnames_path(self):
        surnames_path = SurnameFeature._get_surnames_path()
        self.assertNotEqual(surnames_path, None)
        print(surnames_path)

    def test_get_surnames(self):
        surnames = SurnameFeature._get_surnames()
        self.assertNotEqual(surnames, None)
        print(surnames)
