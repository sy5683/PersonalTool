import logging
from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_profile import StatementProfile


class BOC01Tags(Enum):
    """中国银行 表头"""
    reference_number = "交易流水号[ Transaction reference number ]"
    trade_date = "交易日期[ Transaction Date ]"
    trade_time = "交易时间[ Transaction time ]"
    payee_account_number = "收款人账号[ Payee's Account Number ]"
    payee_name = "收款人名称[ Payee's Name ]"
    payer_account_number = "付款人账号[ Debit Account No. ]"
    payer_name = "付款人名称[ Payer's Name ]"
    reference = "摘要[ Reference ]"
    remark = "交易附言[ Remark ]"
    remarks = "备注[ Remarks ]"
    purpose = "用途[ Purpose ]"
    trade_amount = "交易金额[ Trade Amount ]"
    balance = "交易后余额[ After-transaction balance ]"


class BOC01SpecialTags(Enum):
    """中国银行 特殊表头"""
    account_number = "查询账号[ Inquirer account number ]"


class BOC01Statement(StatementProfile):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("中国银行", statement_path, check_tags=[tag.value for tag in BOC01Tags], **kwargs)

    def parse_statement(self):
        """解析流水"""
        self.account_number = self._get_special_data(BOC01SpecialTags.account_number.value)
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = data[BOC01Tags.reference_number.value]  # 交易流水号
            # noinspection PyBroadException
            try:  # 交易时间
                trade_datetime = data[BOC01Tags.trade_date.value] + data[BOC01Tags.trade_time.value]
                statement.trade_datetime = self._format_date(trade_datetime)
            except Exception:
                logging.warning(f"数据异常，不处理: {data}")
                continue
            statement.account_number = self.account_number  # 开户账号
            if self.account_number == data[BOC01Tags.payee_account_number.value].strip():
                statement.account_name = data[BOC01Tags.payee_name.value]  # 开户名称
                statement.reciprocal_account_name = data[BOC01Tags.payer_name.value]  # 对方账户名称
                statement.reciprocal_account_number = data[BOC01Tags.payer_account_number.value]  # 对方账户号
                statement.receive_amount = abs(NumberUtil.to_amount(data[BOC01Tags.trade_amount.value]))  # 收款金额
            elif self.account_number == data[BOC01Tags.payer_account_number.value].strip():
                statement.account_name = data[BOC01Tags.payer_name.value]  # 开户名称
                statement.reciprocal_account_name = data[BOC01Tags.payee_name.value]  # 对方账户名称
                statement.reciprocal_account_number = data[BOC01Tags.payee_account_number.value]  # 对方账户号
                statement.payment_amount = abs(NumberUtil.to_amount(data[BOC01Tags.trade_amount.value]))  # 付款金额
            if not statement.payment_amount and not statement.receive_amount:
                continue
            abstract_list = [data[BOC01Tags.reference.value], data[BOC01Tags.remark.value],
                             data[BOC01Tags.remarks.value]]
            statement.abstract = "；".join([each for each in abstract_list if each])  # 摘要
            statement.purpose = data[BOC01Tags.purpose.value]  # 用途
            statement.balance = NumberUtil.to_amount(data[BOC01Tags.balance.value])  # 余额
            self.statements.append(statement)
