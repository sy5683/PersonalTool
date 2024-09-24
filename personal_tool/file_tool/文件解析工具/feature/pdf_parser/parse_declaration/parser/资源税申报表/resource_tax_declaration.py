import re

import fitz

from common_util.data_util.number_util.number_util import NumberUtil
from ...entity.declaration import Declaration
from ...entity.declaration_parser import DeclarationParser


class ResourceTaxDeclaration(DeclarationParser):

    def __init__(self, declaration_path: str, **kwargs):
        super().__init__("资源税申报表", declaration_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        with fitz.open(self.pdf_path) as pdf:
            pdf_text = re.sub(r"\s+", "", pdf[0].get_text())
            if re.search("财产和行为税纳税申报表", pdf_text):
                return True
        return False

    def parse(self):
        """解析"""
        try:
            # 申报表页面只有第一张，后面的附表不需要解析
            profile = self.pdf_profiles[0]
            # 申报表只有一个表格，其余的无需处理
            table = profile.tables[0]
        except IndexError:
            raise ValueError("无法在商户结算记录中提取出表格数据")
        for row in range(table.max_rows):
            row_values = table.get_row_values(row)
            try:  # 当前只计算资源税的数据
                assert row_values[1] == "资源税"
            except (AssertionError, IndexError):
                continue
            declaration = Declaration()
            declaration.declaration_type = self.parser_type  # 申报表类型
            declaration.from_date = row_values[3]  # 税款所属时间起
            declaration.to_date = row_values[4]  # 税款所属时间止
            declaration.revenue = NumberUtil.to_amount(row_values[5])  # 申报表收入
            declaration.tax_amount = NumberUtil.to_amount(row_values[7])  # 申报表税额
            self.declarations.append(declaration)
