import re
from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class CBHB02Tags(Enum):
    """渤海银行 表头"""
    reference_number = "交易流水号"
    trade_date = "交易日期"
    trade_time = "交易时间"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    remark = "备注"
    pay_type = "收支标识"
    trade_amount = "交易金额"
    balance = "账户余额"


class CBHB02SpecialTags(Enum):
    """渤海银行 特殊表头"""
    account_name = "账户名称："
    account_number = "账号："


class CBHB02StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("渤海银行", statement_path, check_tags=[tag.value for tag in CBHB02Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        account_name = self._get_special_data(CBHB02SpecialTags.account_name.value)
        self.account_number = re.sub(r"\D+", "", self._get_special_data(CBHB02SpecialTags.account_number.value))
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[CBHB02Tags.reference_number.value]  # 交易流水号
            trade_datetime = data[CBHB02Tags.trade_date.value] + data[CBHB02Tags.trade_time.value]
            statement.trade_datetime = self._format_date(trade_datetime)  # 交易时间
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            statement.reciprocal_account_name = data[CBHB02Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[CBHB02Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = f"{statement.reciprocal_account_name} {data[CBHB02Tags.abstract.value]}"  # 摘要
            statement.purpose = data[CBHB02Tags.remark.value]  # 用途
            if data[CBHB02Tags.pay_type.value] == "收入":
                statement.receive_amount = NumberUtil.to_amount(data[CBHB02Tags.trade_amount.value])  # 收款金额
            elif data[CBHB02Tags.pay_type.value] == "支出":
                statement.payment_amount = NumberUtil.to_amount(data[CBHB02Tags.trade_amount.value])  # 付款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[CBHB02Tags.balance.value])  # 余额
            self.statements.append(statement)
