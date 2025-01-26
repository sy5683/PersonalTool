from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class FC01Tags(Enum):
    """财务公司 表头"""
    reference_number = "交易编号"
    trade_datetime = "日期"
    reciprocal_account_name = "对方账户名称"
    reciprocal_account_number = "对方账户号"
    abstract = "摘要"
    # 【财务公司】无对应【用途】
    payment_amount = "付款金额"
    receive_amount = "收款金额"
    balance = "余额"


class FC01SpecialTags(Enum):
    """财务公司 特殊表头"""
    account_name = "户名："
    account_number = "账户号："


class FC01StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("财务公司", statement_path, check_tags=[tag.value for tag in FC01Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        account_name = self._get_special_data(FC01SpecialTags.account_name.value, relative_col=0)
        account_name = account_name.replace(FC01SpecialTags.account_name.value, "").strip()
        self.account_number = self._get_special_data(FC01SpecialTags.account_number.value, relative_col=0)
        self.account_number = self.account_number.replace(FC01SpecialTags.account_number.value, "").strip()
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[FC01Tags.reference_number.value]  # 交易流水号
            if not statement.reference_number:
                continue
            statement.trade_datetime = self._format_date(data[FC01Tags.trade_datetime.value])  # 交易时间
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            statement.reciprocal_account_name = data[FC01Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[FC01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[FC01Tags.abstract.value]  # 摘要
            statement.purpose = ""  # 用途(【财务公司】无对应用途)
            statement.payment_amount = NumberUtil.to_amount(data[FC01Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[FC01Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[FC01Tags.balance.value])  # 余额
            self.statements.append(statement)
