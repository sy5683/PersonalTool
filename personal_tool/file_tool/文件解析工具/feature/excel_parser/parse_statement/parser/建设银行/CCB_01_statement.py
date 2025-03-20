from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class CCB01Tags(Enum):
    """建设银行 表头"""
    reference_number = "账户明细编号-交易流水号"
    trade_datetime = "交易时间"
    account_name = "本方账户名称"
    account_number = "本方账号"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    remark = "备注"
    trade_amount = "发生额/元"
    balance = "余额/元"


class CCB01SpecialTags(Enum):
    """建设银行 特殊表头"""
    payment_amount = "借方"
    receive_amount = "贷方"


class CCB01StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("建设银行", statement_path, check_tags=[tag.value for tag in CCB01Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        # 建设银行读取的流水格式需要特殊处理：发生额下方有一行分出了付款与收款
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row, tag_row_quantity=2):
            statement = Statement()
            statement.reference_number = data[CCB01Tags.reference_number.value]  # 交易流水号
            statement.trade_datetime = self._format_date(data[CCB01Tags.trade_datetime.value])  # 交易时间
            statement.account_name = data[CCB01Tags.account_name.value]  # 开户名称
            statement.account_number = data[CCB01Tags.account_number.value]  # 开户账号
            statement.reciprocal_account_name = data[CCB01Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[CCB01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[CCB01Tags.remark.value]  # 摘要
            statement.purpose = data[CCB01Tags.abstract.value]  # 用途
            statement.payment_amount = NumberUtil.to_amount(
                data[CCB01Tags.trade_amount.value + CCB01SpecialTags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(
                data[CCB01Tags.trade_amount.value + CCB01SpecialTags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[CCB01Tags.balance.value])  # 余额
            self.statements.append(statement)
            self.account_number = statement.account_number
