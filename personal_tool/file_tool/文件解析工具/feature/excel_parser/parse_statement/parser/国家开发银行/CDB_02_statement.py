from enum import Enum

import xlrd

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class CDB02Tags(Enum):
    """国家开发银行 表头"""
    reference_number = "账户明细编号-交易流水号"
    trade_datetime = "交易时间"
    account_name = "账户名称"
    account_number = "账号"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    remark = "备注"
    payment_amount = "借方发生额（支取）"
    receive_amount = "贷方发生额（收入）"
    balance = "余额"


class CDB02StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("国家开发银行", statement_path, check_tags=[tag.value for tag in CDB02Tags], **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.tag_row is None:
            return False
        # 国开行新格式与建行格式相同，这里选一个特殊列进行判断区分
        workbook = xlrd.open_workbook(self.statement_path)
        worksheet = workbook.sheet_by_name(workbook.sheet_names()[0])
        if "个性化信息名称1" in worksheet.row_values(self.tag_row):
            return False
        return True

    def parse_statement(self):
        """解析流水"""
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[CDB02Tags.reference_number.value]  # 交易流水号
            statement.trade_datetime = self._format_date(data[CDB02Tags.trade_datetime.value])  # 交易时间
            statement.account_name = data[CDB02Tags.account_name.value]  # 开户名称
            statement.account_number = data[CDB02Tags.account_number.value]  # 开户账号
            self.account_number = statement.account_number
            statement.reciprocal_account_name = data[CDB02Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[CDB02Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[CDB02Tags.remark.value]  # 摘要
            statement.purpose = data[CDB02Tags.abstract.value]  # 用途
            statement.payment_amount = NumberUtil.to_amount(data[CDB02Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[CDB02Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[CDB02Tags.balance.value])  # 余额
            self.statements.append(statement)
