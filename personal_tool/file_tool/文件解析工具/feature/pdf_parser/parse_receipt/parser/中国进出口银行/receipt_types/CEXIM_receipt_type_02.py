from common_util.data_util.time_util.time_util import TimeUtil
from .CEXIM_receipt_type import CEXIMReceiptType
from ....entity.receipt import Receipt


class CEXIMReceiptType02(CEXIMReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["项目名称", "工本费/转账汇款手续费/手续费", "金额"]:
            if key not in "".join(self.table.get_row_values(1)):
                return False
        if "合计金额" not in self.table.get_col_values(0):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_time(self._get_word(".*年.*月.*日"))  # 日期
        receipt.payer_account_name = self._get_name(self.table.get_row_values(0)[0])  # 付款人户名
        receipt.payer_account_number = self._get_account(self.table.get_row_values(0)[1])  # 付款人账号
        receipt.amount = self._get_amount(0, 2)  # 金额
        return receipt
