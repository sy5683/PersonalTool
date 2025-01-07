from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class ABC01Tags(Enum):
    """农业银行 表头"""
    # 【农业银行】无对应【交易流水号】
    trade_datetime = "交易时间"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    abstract = "交易用途"
    # 【农业银行】无对应【用途】
    payment_amount = "支出金额"
    receive_amount = "收入金额"
    balance = "账户余额"


class ABC01SpecialTags(Enum):
    """农业银行 特殊表头"""
    account_name = "账户名称"
    account_number = "账户号"


class ABC01StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("农业银行", statement_path, check_tags=[tag.value for tag in ABC01Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        try:
            account_name = self._get_special_data(ABC01SpecialTags.account_name.value, relative_col=2)
            self.account_number = self._get_special_data(ABC01SpecialTags.account_number.value, relative_col=2)
        except ValueError:  # 农行流水文件中可能没有这些值，因此需要特殊处理
            account_name, self.account_number = self._get_abc_account_info()
        assert self.account_number, f"银行流水【{self.statement_name}】未取到农行账号"
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = ""  # 交易流水号(【农业银行】无对应交易流水号)
            statement.trade_datetime = self._format_date(data[ABC01Tags.trade_datetime.value])  # 交易时间
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            reciprocal_account_name = data[ABC01Tags.reciprocal_account_name.value]
            statement.reciprocal_account_name = reciprocal_account_name  # 对方账户名称
            statement.reciprocal_account_number = data[ABC01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = f"{reciprocal_account_name}；{data[ABC01Tags.abstract.value]}"  # 摘要
            statement.purpose = ""  # 用途(【农业银行】无对应用途)
            statement.payment_amount = NumberUtil.to_amount(data[ABC01Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[ABC01Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[ABC01Tags.balance.value])  # 余额
            self.statements.append(statement)
