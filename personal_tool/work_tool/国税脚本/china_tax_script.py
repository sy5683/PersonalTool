from enum import Enum

from common_core.base.tool_base import ToolBase
from feature.china_tax.goods_tax_feature import GoodsTaxFeature


class Operations(Enum):
    claw_goods_tax_code = GoodsTaxFeature.claw_goods_tax_code


class ChinaTaxScript(ToolBase):

    def main(self, function, **kwargs):
        function(**kwargs)


if __name__ == '__main__':
    china_tax_script = ChinaTaxScript()
    china_tax_script.main(Operations.claw_goods_tax_code)
