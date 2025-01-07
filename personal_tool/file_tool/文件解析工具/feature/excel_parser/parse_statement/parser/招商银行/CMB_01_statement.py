from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class CMB01Tags(Enum):
    """招商银行 表头"""
    reference_number = "流水号"
    trade_date = "交易日"
    trade_time = "交易时间"
    reciprocal_account_name = "收(付)方名称"
    reciprocal_account_number = "收(付)方账号"
    trade_type = "交易类型"
    business_abstract = "业务摘要"
    other_abstract = "其它摘要"
    purpose = "用途"
    payment_amount = "借方金额"
    receive_amount = "贷方金额"
    balance = "余额"


class CMB01SpecialTags(Enum):
    """招商银行 特殊表头"""
    account_name_1 = "公司名称"
    account_name_2 = "账号名称"
    account_number = "银行账号"


class CMB01StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("招商银行", statement_path, check_tags=[tag.value for tag in CMB01Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        account_name = self._get_special_data(CMB01SpecialTags.account_name_1.value,
                                              CMB01SpecialTags.account_name_2.value)
        self.account_number = self._get_special_data(CMB01SpecialTags.account_number.value)
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[CMB01Tags.reference_number.value]  # 交易流水号
            trade_datetime = data[CMB01Tags.trade_date.value] + data[CMB01Tags.trade_time.value]
            statement.trade_datetime = self._format_date(trade_datetime)  # 交易时间
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            statement.reciprocal_account_name = data[CMB01Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[CMB01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = data[CMB01Tags.purpose.value]  # 摘要
            abstract_list = [data[CMB01Tags.trade_type.value], data[CMB01Tags.business_abstract.value],
                             data[CMB01Tags.other_abstract.value]]
            statement.purpose = "；".join([each for each in abstract_list if each])  # 用途
            statement.payment_amount = NumberUtil.to_amount(data[CMB01Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[CMB01Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[CMB01Tags.balance.value])  # 余额
            self.statements.append(statement)
