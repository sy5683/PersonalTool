from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .YNRCC_receipt_type import YNRCCReceiptType
from ....entity.receipt import Receipt


class YNRCCReceiptType01(YNRCCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if {"手续费支付账号", "手续费支付账号户名", "手续费收入机构", "手续费大写金额", "手续费小写金额",
            "本金交易摘要"} < set(self.table.get_col_values(0)):
            return True
        return False

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_word("^日期[:：](.*?)$"))  # 日期
        receipt.receipt_number = self._get_word("^交易指令序号[:：](.*?)$")  # 回单编号
        receipt.payer_account_name = self._get_cell_relative("^手续费支付账号户名$").get_value()  # 付款人户名
        receipt.payer_account_number = self._get_cell_relative("^手续费支付账号$").get_value()  # 付款人账号
        receipt.payer_account_bank = self._get_cell_relative("^手续费收入机构$").get_value()  # 付款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^手续费小写金额$").get_value())  # 金额
        receipt.abstract = self._get_cell_relative("^本金交易摘要$").get_value()  # 摘要
        receipt.image = self.image  # 图片
        return receipt
