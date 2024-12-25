import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .FC_receipt_type import FCReceiptType
from ....entity.receipt import Receipt


class FCReceiptType06(FCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["借款单位", "贷款账户号", "委托单位", "合同编号", "开户银行", "人民币元"]:
            if not re.search(key, "".join(self.table.get_col_values(0))):
                return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_word("^.*年.*月.*日$"))  # 日期
        receipt.receipt_number = self._get_word("^交易编号[:：](.*?)$")  # 回单编号
        receipt.serial_number = self._get_cell_relative("^合同编号").get_value()  # 流水号
        receipt.payer_account_name = self._get_cell_relative("^委托单位").get_value()  # 付款人户名
        receipt.payer_account_bank = self._get_cell_relative("^开户银行").get_value()  # 付款人开户银行
        receipt.payee_account_name = self._get_cell_relative("^借款单位").get_value()  # 收款人户名
        receipt.payee_account_number = self._get_cell_relative("^贷款账户号").get_value()  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^人民币元", 2).get_value())  # 金额
        return receipt
