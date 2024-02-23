import logging
import typing
from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_profile import StatementProfile


class CDB01Tags(Enum):
    """国开行 表头"""
    reference_number = "交易参考号"
    trade_datetime = "交易时间"
    payment_or_receive = "收入/支出标志"
    payee_account_number = "收款账号"
    payee_name = "收款户名"
    payer_account_number = "付款账号"
    payer_name = "付款户名"
    abstract = "摘要"
    # 【国开行】无对应【用途】
    trade_amount = "发生额（元）"
    balance = "交易后余额（元）"


class CDB01(StatementProfile):

    def __init__(self, statement_path: str, tag_row: int, **kwargs):
        super().__init__("国开行", statement_path, tag_row, **kwargs)

    @staticmethod
    def get_check_tags() -> typing.List[str]:
        """获取校验用的表头"""
        return [tag.value for tag in CDB01Tags]

    def parse_statement(self):
        """解析流水"""
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[CDB01Tags.reference_number.value]  # 交易流水号
            # noinspection PyBroadException
            try:  # 交易时间
                statement.trade_datetime = self._format_date(data[CDB01Tags.trade_datetime.value])
            except Exception:  
                logging.warning(f"数据异常，不处理: {data}")
                continue
            if data[CDB01Tags.payment_or_receive.value] == "收入":
                statement.account_name = data[CDB01Tags.payee_name.value]  # 开户名称
                statement.account_number = data[CDB01Tags.payee_account_number.value]  # 开户账号
                statement.reciprocal_account_name = data[CDB01Tags.payer_name.value]  # 对方账户名称
                statement.reciprocal_account_number = data[CDB01Tags.payer_account_number.value]  # 对方账户号
                statement.receive_amount = NumberUtil.to_amount(data[CDB01Tags.trade_amount.value])  # 收款金额
            elif data[CDB01Tags.payment_or_receive.value] == "支出":
                statement.account_name = data[CDB01Tags.payer_name.value]  # 开户名称
                statement.account_number = data[CDB01Tags.payer_account_number.value]  # 开户账号
                statement.reciprocal_account_name = data[CDB01Tags.payee_name.value]  # 对方账户名称
                statement.reciprocal_account_number = data[CDB01Tags.payee_account_number.value]  # 对方账户号
                statement.payment_amount = NumberUtil.to_amount(data[CDB01Tags.trade_amount.value])  # 付款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            if self.account_number is None and statement.account_number:
                self.account_number = statement.account_number
            statement.abstract = data[CDB01Tags.abstract.value]  # 摘要
            statement.purpose = ""  # 用途(【国开行】无对应用途)
            statement.balance = NumberUtil.to_amount(data[CDB01Tags.balance.value])  # 余额
            self.statements.append(statement)
