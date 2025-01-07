from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class CMBC01Tags(Enum):
    """民生银行 表头"""
    reference_number = "交易流水号"
    trade_datetime = "交易时间"
    reciprocal_account_name = "对方账号名称"
    reciprocal_account_number = "对方账号"
    abstract = "客户附言"
    # 【民生银行】无对应【用途】
    payment_amount = "借方发生额"
    receive_amount = "贷方发生额"
    balance = "账户余额"


class CMBC01SpecialTags(Enum):
    """民生银行 特殊表头"""
    account_name = "账户名称:"
    account_number = "^账号:"


class CMBC01StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("民生银行", statement_path, check_tags=[tag.value for tag in CMBC01Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        account_name = self._get_special_data(CMBC01SpecialTags.account_name.value)
        self.account_number = self._get_special_data(CMBC01SpecialTags.account_number.value)
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[CMBC01Tags.reference_number.value]  # 交易流水号
            statement.trade_datetime = self._format_date(data[CMBC01Tags.trade_datetime.value])  # 交易时间
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            reciprocal_account_name = data[CMBC01Tags.reciprocal_account_name.value]
            statement.reciprocal_account_name = reciprocal_account_name  # 对方账户名称
            statement.reciprocal_account_number = data[CMBC01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[CMBC01Tags.abstract.value]  # 摘要
            statement.purpose = "" # 用途(【民生银行】无对应【用途】)
            statement.payment_amount = NumberUtil.to_amount(data[CMBC01Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[CMBC01Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[CMBC01Tags.balance.value])  # 余额
            self.statements.append(statement)
