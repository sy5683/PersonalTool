import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .CMB_receipt_type import CMBReceiptType
from ....entity.receipt import Receipt


class CMBReceiptType03(CMBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.max_rows not in [1, 2] or self.table.max_cols != 1:
            return False
        if not re.search("[出入]账回单", self.table.get_cell(0, 0).get_value()):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        # 招商银行这个格式的回单数据全在一个大的表格单元格中，重新加载其为word数据后使用word方法解析
        self.words += PdfUtil.merge_words(self.table.cells[0].words, 10)
        receipt.date = TimeUtil.format_to_str(self._get_word("^交易日期[:：](.*?)$"))  # 日期
        receipt.receipt_number = self._get_word(r"回单编号[:：](.*?)$")  # 回单编号
        receipt.serial_number = self._get_word(r"交易流水[:：](.*?)$")  # 流水号
        receipt.payer_account_name = self._get_word("^付款人[:：](.*?)$")  # 付款人户名
        receipt.payer_account_number = self._get_word("^付款账号[:：](.*?)$")  # 付款人账号
        receipt.payer_account_bank = self._get_word("^付款开户行[:：](.*?)$")  # 付款人开户银行
        receipt.payee_account_name = self._get_word("^收款人[:：](.*?)$")  # 收款人户名
        receipt.payee_account_number = self._get_word("^收款账号[:：](.*?)$")  # 收款人账号
        receipt.payee_account_bank = self._get_word("^收款开户行[:：](.*?)$")  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_word("^交易金额[(（]小写[)）][:：](.*?)$"))  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt
