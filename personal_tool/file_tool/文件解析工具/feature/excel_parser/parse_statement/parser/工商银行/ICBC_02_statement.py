import logging
from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class ICBC02Tags(Enum):
    """工商银行 表头"""
    # 【工商银行】无对应【交易流水号】
    trade_datetime = "日期"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    # 【工商银行】无对应【用途】
    payment_amount = "借方发生额"
    receive_amount = "贷方发生额"
    balance = "余额"


class ICBC02SpecialTags(Enum):
    """工商银行 特殊表头"""
    account_name = "户名: "
    account_number = "账号: "


class ICBC02Statement(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("工商银行", statement_path, check_tags=[tag.value for tag in ICBC02Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        account_name = self._get_special_data(ICBC02SpecialTags.account_name.value)
        self.account_number = self._get_special_data(ICBC02SpecialTags.account_number.value).strip()
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = ""  # 交易流水号(【工商银行】无对应交易流水号)
            # noinspection PyBroadException
            try:  # 交易时间
                statement.trade_datetime = self._format_date(data[ICBC02Tags.trade_datetime.value])
            except Exception:
                logging.warning(f"数据异常，不处理: {data}")
                continue
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            statement.reciprocal_account_name = data[ICBC02Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[ICBC02Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[ICBC02Tags.abstract.value]  # 摘要
            statement.purpose = ""  # 用途(【工商银行】无对应用途)
            statement.payment_amount = NumberUtil.to_amount(data[ICBC02Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[ICBC02Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[ICBC02Tags.balance.value])  # 余额
            self.statements.append(statement)
