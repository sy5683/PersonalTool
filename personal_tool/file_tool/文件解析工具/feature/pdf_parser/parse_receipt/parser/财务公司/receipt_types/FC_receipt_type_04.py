import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .FC_receipt_type import FCReceiptType
from ....entity.receipt import Receipt


class FCReceiptType04(FCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["类型", "本金", "利率", "利息"]:
            if not re.search(key, "".join(self.table.get_row_values(0))):
                return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_word("^.*年.*月.*日$"))  # 日期
        receipt.receipt_number = self._get_word("^交易编号[:：](.*?)$")  # 回单编号
        receipt.payer_account_name = self._get_word("^借款单位名称[:：](.*?)$")  # 付款人户名
        receipt.payer_account_number = self._get_word("^账号[:：](.*?)$")  # 付款人账号
        receipt.payee_account_name = self._get_word("^委托单位名称[:：](.*?)$")  # 收款人户名
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^利息总额", 3).get_value())  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt
