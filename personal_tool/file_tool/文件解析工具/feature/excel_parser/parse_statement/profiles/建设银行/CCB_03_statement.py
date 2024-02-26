import logging
import typing
from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_profile import StatementProfile


class CCB03Tags(Enum):
    """建设银行 表头"""
    reference_number = "账户明细编号-交易流水号"
    trade_datetime = "交易时间"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    remark = "备注"
    payment_amount = "借方发生额/元(支取)"
    receive_amount = "贷方发生额/元(收入)"
    balance = "余额"


class CCB03SpecialTags(Enum):
    """建设银行 特殊表头"""
    account_number = "账　　号"
    account_name = "账户名称"


class CCB03Statement(StatementProfile):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("建设银行", statement_path, **kwargs)

    @staticmethod
    def get_check_tags() -> typing.List[str]:
        """获取校验用的表头"""
        return [tag.value for tag in CCB03Tags]

    def parse_statement(self):
        """解析流水"""
        account_name = self._get_special_data(CCB03SpecialTags.account_name.value)
        self.account_number = self._get_special_data(CCB03SpecialTags.account_number.value)
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[CCB03Tags.reference_number.value]  # 交易流水号
            # noinspection PyBroadException
            try:  # 交易时间
                statement.trade_datetime = self._format_date(data[CCB03Tags.trade_datetime.value])
            except Exception:  
                logging.warning(f"数据异常，不处理: {data}")
                continue
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            statement.reciprocal_account_name = data[CCB03Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[CCB03Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[CCB03Tags.remark.value]  # 摘要
            statement.purpose = data[CCB03Tags.abstract.value]  # 用途
            statement.payment_amount = NumberUtil.to_amount(data[CCB03Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[CCB03Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[CCB03Tags.balance.value])  # 余额
            self.statements.append(statement)
