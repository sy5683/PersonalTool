import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .duty_paid_proof_type import DutyPaidProofType
from ....entity.invoice import Invoice


class DutyPaidProofType01(DutyPaidProofType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["原凭证号", "税种", "品目名称", "税款所属时期", "入[(（]退[)）]库日期", "实缴[(（]退[)）]金额"]:
            if not re.search(key, "".join(self.table.get_row_values(1))):
                return False
        return True

    def get_invoice(self) -> Invoice:
        """解析"""
        invoice = Invoice()
        invoice.date = TimeUtil.format_to_str(self._get_word("^填发日期[:：](.*?)$"))  # 日期
        invoice.details = self._get_details(1)  # 多行明细
        invoice.amount = NumberUtil.to_amount(self._get_cell_relative("^金额合计$", 2).get_value())  # 金额
        return invoice
