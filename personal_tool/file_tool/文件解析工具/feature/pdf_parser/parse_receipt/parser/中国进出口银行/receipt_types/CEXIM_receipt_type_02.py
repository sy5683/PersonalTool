from common_util.data_util.number_util.number_util import NumberUtil
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
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self._get_word("^.*年.*月.*日$"))  # 日期
        receipt.receipt_number = self._get_word(r"^[a-zA-Z\d+]+$")  # 回单编号
        receipt.serial_number = self._get_word("^流水号[:：](.*?)$")  # 流水号
        payer_account_row_cells = self.table.get_row_cells(0)
        receipt.payer_account_name = self._get_name(payer_account_row_cells[0].get_value())  # 付款人户名
        receipt.payer_account_number = self._get_account(payer_account_row_cells[1].get_value())  # 付款人账号
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^合计金额$", 2).get_value())  # 金额
        return receipt
