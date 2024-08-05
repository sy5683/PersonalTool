from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CCB_receipt_type import CCBReceiptType
from ....entity.receipt import Receipt


class CCBReceiptType06(CCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["申请客户名称", "业务编号"]:
            if key not in "".join(self.table.get_row_values(0)):
                return False
        if not {"付款账号", "收款账号"} < set(self.table.get_row_values(1)):
            return False
        if len(self.table.get_row_values(5)) != 4:
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self._get_word("^.*年.*月.*日$"))  # 日期
        receipt.receipt_number = self._get_word(r"^[a-zA-Z\d+]+$")  # 回单编号
        receipt.serial_number = self._get_word("^流水号[:：](.*?)$")  # 流水号
        number_row_cells = self.table.get_row_cells(1)
        name_row_cells = self.table.get_row_cells(2)
        if number_row_cells[0].get_value() == "付款账号":
            receipt.payer_account_name = name_row_cells[1].get_value()  # 付款人户名
            receipt.payer_account_number = number_row_cells[1].get_value()  # 付款人账号
            receipt.payee_account_name = name_row_cells[3].get_value()  # 收款人户名
            receipt.payee_account_number = number_row_cells[3].get_value()  # 收款人账号
        elif number_row_cells[0].get_value() == "收款账号":
            receipt.payer_account_name = name_row_cells[3].get_value()  # 付款人户名
            receipt.payer_account_number = number_row_cells[3].get_value()  # 付款人账号
            receipt.payee_account_name = name_row_cells[1].get_value()  # 收款人户名
            receipt.payee_account_number = number_row_cells[1].get_value()  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_cell(5, 3).get_value())  # 金额
        return receipt
