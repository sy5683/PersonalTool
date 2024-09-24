import logging

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from ...entity.declaration import Declaration
from ...entity.declaration_parser import DeclarationParser


class ValueAddTaxDeclaration(DeclarationParser):

    def __init__(self, declaration_path: str, **kwargs):
        super().__init__("增值税申报表", declaration_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("增值税及附加税费申报表")

    def parse(self):
        """解析"""
        try:
            # 申报表页面只有第一张，后面的附表不需要解析
            profile = self.pdf_profiles[0]
            # 申报表只有一个表格，其余的无需处理
            table = profile.tables[0]
            words = profile.words
        except IndexError:
            raise ValueError("无法在商户结算记录中提取出表格数据")
        declaration = Declaration()
        declaration.declaration_type = self.parser_type  # 申报表类型
        try:
            tax_dates = PdfUtil.filter_word(words, "^税款所属时间[:：]自(.*?)$").split("至")
            declaration.from_date = tax_dates[0]  # 税款所属时间起
            declaration.to_date = tax_dates[1]  # 税款所属时间止
        except AttributeError:
            logging.warning(f"申报表中无法查找到指定的税款所属时间")
        declaration.revenue = NumberUtil.to_amount(
            table.get_cell_relative("按适用税率计税销售额", 2).get_value())  # 申报表收入
        declaration.tax_amount = NumberUtil.to_amount(table.get_cell_relative("^销项税额$", 2).get_value())  # 申报表税额
        self.declarations.append(declaration)
