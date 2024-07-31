from common_core.base.test_base import TestBase
from common_util.data_util.list_util.list_util import ListUtil


class ListUtilTestCase(TestBase):

    def test_check_contain(self):
        errors = ListUtil.check_contain([1, 2, 3, 4, 5], [1, 2, 3, 4, 10])
        self.assertNotEqual(errors, None)
        print(errors)

    def test_get_combinations(self):
        combinations = ListUtil.get_combinations([1, 2, 3, 4])
        self.assertNotEqual(combinations, None)
        for combination in combinations:
            print(combination)
