from common_core.base.test_base import TestBase
from common_util.data_util.list_util.list_util import ListUtil


class ListUtilTestCase(TestBase):

    def test_check_contain(self):
        errors = ListUtil.check_contain([1, 2, 3, 4, 5], [1, 2, 3, 4, 10])
        self.assertNotEqual(errors, None)
        print(errors)

    def test_deduplicate(self):
        deduplicate_listing = ListUtil.deduplicate([1, 5, 5, 7, 3, 1, 6])
        self.assertNotEqual(deduplicate_listing, None)
        print(deduplicate_listing)

    def test_get_combinations(self):
        combinations = ListUtil.get_combinations([1, 2, 3, 4])
        self.assertNotEqual(combinations, None)
        for combination in combinations:
            print(combination)
