import logging
import typing
from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_profile import StatementProfile


class ICBC01Tags(Enum):
    """工商银行 表头"""
    # 【工商银行】无对应【交易流水号】
    trade_datetime = "交易时间"
    account_number = "本方账号"
    reciprocal_account_name = "对方单位"
    reciprocal_account_number = "对方账号"
    abstract = "摘要"
    remark = "附言"
    purpose = "用途"
    payment_amount = "转出金额"
    receive_amount = "转入金额"
    balance = "余额"


class ICBC01Statement(StatementProfile):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("工商银行", statement_path, **kwargs)

    @staticmethod
    def get_check_tags() -> typing.List[str]:
        """获取校验用的表头"""
        return [tag.value for tag in ICBC01Tags]

    def parse_statement(self):
        """解析流水"""
        assert self.company_name, "工行流水需要传入公司名称作为开户名称"
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = ""  # 交易流水号(【工商银行】无对应交易流水号)
            # noinspection PyBroadException
            try:  # 交易时间
                statement.trade_datetime = self._format_date(data[ICBC01Tags.trade_datetime.value])
            except Exception:  
                logging.warning(f"数据异常，不处理: {data}")
                continue
            # 工行下载时有异常情况，下载时选项没有开户名称，因此工行的开户名称通过表单参数传递
            statement.account_name = self.company_name  # 开户名称
            statement.account_number = data[ICBC01Tags.account_number.value]  # 开户账号
            self.account_number = statement.account_number
            statement.reciprocal_account_name = data[ICBC01Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[ICBC01Tags.reciprocal_account_number.value]  # 对方账户号
            statement.abstract = f"{data[ICBC01Tags.abstract.value]}；{data[ICBC01Tags.remark.value]}".strip("；")  # 摘要
            statement.purpose = data[ICBC01Tags.purpose.value]  # 用途
            statement.payment_amount = NumberUtil.to_amount(data[ICBC01Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[ICBC01Tags.receive_amount.value])  # 收款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[ICBC01Tags.balance.value])  # 余额
            self.statements.append(statement)
