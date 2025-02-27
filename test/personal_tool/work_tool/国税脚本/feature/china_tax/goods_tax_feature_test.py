from common_core.base.test_base import TestBase
from common_util.code_util.selenium_util.selenium_util import SeleniumUtil
from common_util.code_util.selenium_util.selenium_utils.entity.selenium_config import SeleniumConfig
from common_util.data_util.object_util.object_util import ObjectUtil
from personal_tool.work_tool.国税脚本.feature.china_tax.goods_tax_feature import GoodsTaxFeature


class GoodsTaxFeatureTestCase(TestBase):

    def setUp(self):
        self.browser_title = "发票开具"

    def test_expand_code_tree(self):
        SeleniumUtil.switch_window(SeleniumConfig(), self.browser_title)
        GoodsTaxFeature._expand_code_tree()

    def test_get_goods_tax_codes(self):
        SeleniumUtil.switch_window(SeleniumConfig(), self.browser_title)
        for goods_tax_code in GoodsTaxFeature._get_goods_tax_codes():
            print(goods_tax_code)

    def test_get_goods_tax_name(self):
        SeleniumUtil.switch_window(SeleniumConfig(), self.browser_title)
        print(GoodsTaxFeature._get_goods_tax_name("1020201030000000000"))

    def test_get_goods_tax_map(self):
        goods_tax_map = GoodsTaxFeature._get_goods_tax_map()
        self.assertNotEqual(goods_tax_map, None)
        ObjectUtil.print_object(goods_tax_map)
