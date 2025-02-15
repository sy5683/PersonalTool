from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class BCM01Tags(Enum):
    """交通银行 表头"""
    # 【交通银行】无对应【交易流水号】
    trade_datetime = "交易时间"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    # 【交通银行】无对应【用途】
    trade_amount = "发生额"
    balance = "余额"


class BCM01SpecialTags(Enum):
    """交通银行 特殊表头"""
    account_name = "户  名:"
    account_number = "查询账号:"
    payment_mark = "借贷标志"


class BCM01StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("交通银行", statement_path, check_tags=[tag.value for tag in BCM01Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        account_name = self._get_special_data(BCM01SpecialTags.account_name.value)
        self.account_number = self._get_special_data(BCM01SpecialTags.account_number.value)
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = ""  # 交易流水号(【交通银行】无对应交易流水号)
            statement.trade_datetime = self._format_date(data[BCM01Tags.trade_datetime.value])  # 交易时间
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            statement.reciprocal_account_name = data[BCM01Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[BCM01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[BCM01Tags.abstract.value]  # 摘要
            statement.purpose = ""  # 用途(【交通银行】无对应用途)
            if data[BCM01SpecialTags.payment_mark.value] == "借":
                statement.payment_amount = NumberUtil.to_amount(data[BCM01Tags.trade_amount.value])  # 付款金额
            elif data[BCM01SpecialTags.payment_mark.value] == "贷":
                statement.receive_amount = NumberUtil.to_amount(data[BCM01Tags.trade_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[BCM01Tags.balance.value])  # 余额
            self.statements.append(statement)
