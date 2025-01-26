from enum import Enum

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from ...entity.statement import Statement
from ...entity.statement_parser import StatementParser


class ABC01Tags(Enum):
    """农业银行 表头"""
    # 【农业银行】无对应【交易流水号】
    trade_datetime = "交易时间"
    reciprocal_account_name = "对方户名"
    reciprocal_account_number = "对方账号"
    payment_amount = "支出金额"
    receive_amount = "收入金额"
    balance = "账户余额"


class ABC01SpecialTags(Enum):
    """农业银行 特殊表头"""
    abstract = "摘要"
    purpose = "交易用途"
    account_name_1 = "账户名称"
    account_number_1 = "账户号"
    account_name_2 = "户名:"
    account_number_2 = "账号:"


class ABC01StatementParser(StatementParser):

    def __init__(self, statement_path: str, **kwargs):
        super().__init__("农业银行", statement_path, check_tags=[tag.value for tag in ABC01Tags], **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.tag_row is None:
            return False
        # 农行有两个可能会只有一个的特殊表头，这里新增一个特殊条件进行判断区分
        worksheet = self._get_worksheet()
        tags = worksheet.row_values(self.tag_row)
        if ABC01SpecialTags.abstract.value not in tags and ABC01SpecialTags.purpose.value not in tags:
            return False
        # 农业银行与四川农村商业银行格式相同，这里新增一个特殊条件进行判断区分
        if worksheet.cell_value(0, 0) != "账户明细":
            return False
        return True

    def parse_statement(self):
        """解析流水"""
        try:
            worksheet = self._get_worksheet()
            special_values = [each for each in worksheet.row_values(2) if isinstance(each, str)]
            if ABC01SpecialTags.account_name_1.value in special_values:
                account_name = self._get_special_data(ABC01SpecialTags.account_name_1.value, relative_col=2)
                self.account_number = self._get_special_data(ABC01SpecialTags.account_number_1.value, relative_col=2)
            elif ABC01SpecialTags.account_name_2.value in "".join(special_values):
                account_name = self._get_special_data(ABC01SpecialTags.account_name_2.value, relative_col=0)
                account_name = account_name.replace(ABC01SpecialTags.account_name_2.value, "").strip()
                self.account_number = self._get_special_data(ABC01SpecialTags.account_number_2.value, relative_col=0)
                self.account_number = self.account_number.replace(ABC01SpecialTags.account_number_2.value, "").strip()
            else:
                raise ValueError
        except ValueError:  # 农行流水文件中可能没有这些值，因此需要特殊处理
            account_name, self.account_number = self._get_abc_account_info()
        # assert self.account_number, f"银行流水【{self.statement_name}】未取到农行账号"  # TODO
        for data in ExcelUtil.get_data_list(self.statement_path, tag_row=self.tag_row):
            statement = Statement()
            statement.reference_number = ""  # 交易流水号(【农业银行】无对应交易流水号)
            statement.trade_datetime = self._format_date(data[ABC01Tags.trade_datetime.value])  # 交易时间
            statement.account_name = account_name  # 开户名称
            statement.account_number = self.account_number  # 开户账号
            statement.reciprocal_account_name = data[ABC01Tags.reciprocal_account_name.value]  # 对方账户名称
            statement.reciprocal_account_number = data[ABC01Tags.reciprocal_account_number.value]  # 对方账户号
            # 摘要
            abstract = data.get(ABC01SpecialTags.abstract.value, "")
            abstract = abstract if abstract else data.get(ABC01SpecialTags.purpose.value, "")
            statement.abstract = f"{statement.reciprocal_account_name}；{abstract}" if abstract else ""
            statement.purpose = ""  # 用途(【农业银行】无对应用途)
            statement.payment_amount = NumberUtil.to_amount(data[ABC01Tags.payment_amount.value])  # 付款金额
            statement.receive_amount = NumberUtil.to_amount(data[ABC01Tags.receive_amount.value])  # 收款金额
            if not statement.trade_datetime:
                continue
            if not statement.payment_amount and not statement.receive_amount:
                continue
            statement.balance = NumberUtil.to_amount(data[ABC01Tags.balance.value])  # 余额
            self.statements.append(statement)
