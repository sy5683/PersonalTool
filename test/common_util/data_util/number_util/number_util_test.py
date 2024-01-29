from common_core.base.test_base import TestBase
from common_util.data_util.number_util.number_util import NumberUtil


class NumberUtilTestCase(TestBase):

    def test_to_account(self):
        account = NumberUtil.to_account(123456.789)
        self.assertNotEqual(account, None)
        print(account)

    def test_to_amount(self):
        amount = NumberUtil.to_amount("123,456.789")
        self.assertNotEqual(amount, None)
        print(amount)
