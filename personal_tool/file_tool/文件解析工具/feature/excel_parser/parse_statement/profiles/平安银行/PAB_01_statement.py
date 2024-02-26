import logging
import typing
from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_profile import StatementProfile


class PAB01Tags(Enum):
    """平安银行 表头"""
    reference_number = "交易流水号"
    trade_date = "交易日期"
    account_number = "账号"
    reciprocal_account_name = "对方账户名称"
    reciprocal_account_number = "对方账户"
    abstract = "摘要"
    purpose = "用途"
    payment_amount = "借"
    receive_amount = "贷"
    balance = "账户余额"


class PAB01Statement(StatementProfile):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("平安银行", statement_path, **kwargs)

    @staticmethod
    def get_check_tags() -> typing.List[str]:
        """获取校验用的表头"""
        return [tag.value for tag in PAB01Tags]

    def parse_statement(self):
        """解析流水"""
        for excel in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = excel[PAB01Tags.reference_number.value]  # 交易流水号
            # noinspection PyBroadException
            try:  # 交易时间
                statement.trade_datetime = self._format_date(excel[PAB01Tags.trade_date.value])
            except Exception:  
                logging.warning(f"数据异常，不处理: {excel}")
                continue
            statement.account_name = ""  # 开户名称(【平安银行】无对应开户名称)
            statement.account_number = excel[PAB01Tags.account_number.value]  # 开户账号
            self.account_number = statement.account_number
            statement.reciprocal_account_name = excel[PAB01Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = excel[PAB01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = excel[PAB01Tags.abstract.value]  # 摘要
            statement.purpose = excel[PAB01Tags.purpose.value]  # 用途
            statement.payment_amount = NumberUtil.to_amount(excel[PAB01Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(excel[PAB01Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(excel[PAB01Tags.balance.value])  # 余额
            self.statements.append(statement)
