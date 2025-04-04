from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class SPDB01Tags(Enum):
    """浦发银行 表头"""
    reference_number = "交易流水号"
    trade_date = "交易日期"
    trade_time = "交易时间"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    remark = "备注"
    payment_amount = "借方金额"
    receive_amount = "贷方金额"
    balance = "余额"


class SPDB01SpecialTags(Enum):
    """浦发银行 特殊表头"""
    account_name = "账户名称"
    account_number = "账号"


class SPDB01StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("浦发银行", statement_path, check_tags=[tag.value for tag in SPDB01Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        account_name = self._get_special_data(SPDB01SpecialTags.account_name.value)
        self.account_number = self._get_special_data(SPDB01SpecialTags.account_number.value)
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[SPDB01Tags.reference_number.value]  # 交易流水号
            trade_datetime = data[SPDB01Tags.trade_date.value] + data[SPDB01Tags.trade_time.value]
            statement.trade_datetime = self._format_date(trade_datetime)  # 交易时间
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            statement.reciprocal_account_name = data[SPDB01Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[SPDB01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[SPDB01Tags.abstract.value]  # 摘要
            statement.purpose = data[SPDB01Tags.remark.value]  # 用途
            statement.payment_amount = NumberUtil.to_amount(data[SPDB01Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[SPDB01Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[SPDB01Tags.balance.value])  # 余额
            self.statements.append(statement)
