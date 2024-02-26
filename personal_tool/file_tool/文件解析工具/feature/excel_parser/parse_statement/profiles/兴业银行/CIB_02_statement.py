import logging
import typing
from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_profile import StatementProfile


class CIB02Tags(Enum):
    """兴业银行 表头"""
    reference_number = "银行流水号"
    trade_datetime = "交易时间"
    account_name = "户名"
    account_number = "账号"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    # 【兴业银行】无对应【用途】
    payment_amount = "借方金额(支出)"
    receive_amount = "贷方金额(收入)"
    balance = "账户余额"


class CIB02Statement(StatementProfile):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("兴业银行", statement_path, **kwargs)

    @staticmethod
    def get_check_tags() -> typing.List[str]:
        """获取校验用的表头"""
        return [tag.value for tag in CIB02Tags]

    def parse_statement(self):
        """解析流水"""
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[CIB02Tags.reference_number.value]  # 交易流水号
            # noinspection PyBroadException
            try:  # 交易时间
                statement.trade_datetime = self._format_date(data[CIB02Tags.trade_datetime.value])
            except Exception:  
                logging.warning(f"数据异常，不处理: {data}")
                continue
            statement.account_name = data[CIB02Tags.account_name.value]  # 开户名称
            statement.account_number = data[CIB02Tags.account_number.value]  # 开户账号
            self.account_number = statement.account_number
            statement.reciprocal_account_name = data[CIB02Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[CIB02Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[CIB02Tags.abstract.value]  # 摘要
            statement.purpose = ""  # 用途(【兴业银行】无对应用途)
            statement.payment_amount = NumberUtil.to_amount(data[CIB02Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[CIB02Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[CIB02Tags.balance.value])  # 余额
            self.statements.append(statement)
