from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CBHB_receipt_type import CBHBReceiptType
from ....entity.receipt import Receipt


class CBHBReceiptType02(CBHBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if "企业网上银行业务收费回单" not in self.table.get_cell(0, 0).get_value():
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_cell_relative("^交易日期[:：]$").get_value())  # 日期
        receipt.serial_number = self._get_cell_relative(r"^渠道流水号[:：]$").get_value()  # 流水号
        receipt.payer_account_name = self._get_cell_relative("^付款人名称[:：]$").get_value()  # 付款人户名
        receipt.payer_account_number = self._get_cell_relative("^付款人账号[:：]$").get_value()  # 付款人账号
        receipt.payer_account_bank = self._get_cell_relative("^付款人开户行[:：]$").get_value()  # 付款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^小写金额[:：]$").get_value())  # 金额
        return receipt
