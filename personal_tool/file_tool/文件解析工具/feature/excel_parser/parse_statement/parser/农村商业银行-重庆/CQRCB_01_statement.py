from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class CQRCB01Tags(Enum):
    """重庆农村商业银行 表头"""
    reference_number = "交易流水号"
    trade_datetime = "交易日期"
    # 【重庆农村商业银行】无对应【开户名称】
    account_number = "交易账号"
    reciprocal_account_name = "对方账户名"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    purpose = "用途"
    payment_amount = "支出金额"
    receive_amount = "收入金额"
    balance = "余额"


class CQRCB01StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("重庆农村商业银行", statement_path, check_tags=[tag.value for tag in CQRCB01Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[CQRCB01Tags.reference_number.value]  # 交易流水号
            statement.trade_datetime = self._format_date(data[CQRCB01Tags.trade_datetime.value])  # 交易时间
            # 重庆农村商业银行下载文件中没有开户名称，因此重庆农村商业银行的开户名称通过表单参数传递
            statement.account_name = self.company_name  # 开户名称
            statement.account_number = data[CQRCB01Tags.account_number.value]  # 开户账号
            statement.reciprocal_account_name = data[CQRCB01Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[CQRCB01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[CQRCB01Tags.abstract.value]  # 摘要
            statement.purpose = data[CQRCB01Tags.purpose.value]  # 用途
            statement.payment_amount = NumberUtil.to_amount(data[CQRCB01Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[CQRCB01Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[CQRCB01Tags.balance.value])  # 余额
            self.statements.append(statement)
            self.account_number = statement.account_number
