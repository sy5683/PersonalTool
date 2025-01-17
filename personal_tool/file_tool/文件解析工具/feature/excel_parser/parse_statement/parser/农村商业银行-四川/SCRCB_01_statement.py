import re
from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class SCRCB01Tags(Enum):
    """四川农村商业银行 表头"""
    reference_number = "交易流水号"
    trade_date = "交易日期"
    trade_time = "交易日期"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    # 【四川农村商业银行】无对应【用途】
    payment_amount = "支出金额"
    receive_amount = "收入金额"
    balance = "账户余额"


class SCRCB01SpecialTags(Enum):
    """四川农村商业银行 特殊表头"""
    account_name = "户名[:：]"
    account_number = "账号[:：]"


class CQRCB01StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("四川农村商业银行", statement_path, check_tags=[tag.value for tag in SCRCB01Tags], **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.tag_row is None:
            return False
        # 四川农村商业银行与农业银行格式相同，这里新增几个特殊条件进行判断区分
        worksheet = self._get_worksheet()
        cell = worksheet.cell_value(1, 0)
        for special_tag in [each.value for each in SCRCB01SpecialTags]:
            if not re.search(special_tag, cell):
                return False
        if worksheet.cell_value(0, 0) != "四川农信账户交易明细":
            return False
        return True

    def parse_statement(self):
        """解析流水"""
        worksheet = self._get_worksheet()
        cell = worksheet.cell_value(1, 0)
        account_name = re.search(rf"{SCRCB01SpecialTags.account_name.value}(.*?)\n", cell).group(1).strip()
        self.account_number = re.search(rf"{SCRCB01SpecialTags.account_number.value}(.*?)\n", cell).group(1).strip()
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[SCRCB01Tags.reference_number.value]  # 交易流水号
            trade_datetime = data[SCRCB01Tags.trade_date.value] + data[SCRCB01Tags.trade_time.value]
            statement.trade_datetime = self._format_date(trade_datetime)  # 交易时间
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            statement.reciprocal_account_name = data[SCRCB01Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[SCRCB01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[SCRCB01Tags.abstract.value]  # 摘要
            # 【四川农村商业银行】无对应【用途】
            statement.payment_amount = NumberUtil.to_amount(data[SCRCB01Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[SCRCB01Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[SCRCB01Tags.balance.value])  # 余额
            self.statements.append(statement)
