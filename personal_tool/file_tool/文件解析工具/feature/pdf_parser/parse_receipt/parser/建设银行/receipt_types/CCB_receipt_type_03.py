import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .CCB_receipt_type import CCBReceiptType
from ....entity.receipt import Receipt


class CCBReceiptType03(CCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.max_rows != 1 or self.table.max_cols != 1:
            return False
        if not re.search("纳税人全称及", self.table.get_cell(0, 0).get_value()):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        # 建设银行这个格式的回单数据全在一个大的表格单元格中，重新加载其为word数据后使用word方法解析
        self.words += PdfUtil.merge_words(self.table.cells[0].words, 10)
        receipt.date = TimeUtil.format_to_str(self._get_word("^转账日期[:：](.*?)$"))  # 日期
        receipt.receipt_number = self._get_word(r"^凭证字号[:：](.*?)$")  # 回单编号
        receipt.serial_number = self._get_word("^缴款书交易流水号[:：](.*?)$")  # 流水号
        receipt.payer_account_name = self._get_word("^付款人全称[:：](.*?)$")  # 付款人户名
        receipt.payer_account_number = self._get_word("^付款人账号[:：](.*?)$")  # 付款人账号
        receipt.payer_account_bank = self._get_word("^付款人开户银行[:：](.*?)$")  # 付款人开户银行
        receipt.payee_account_name = self._get_word("^征收机关名称[(（]委托方[)）][:：](.*?)$")  # 收款人户名
        receipt.amount = NumberUtil.to_amount(self._get_word("^小写[(（]合计[)）]金额[:：](.*?)$"))  # 金额
        return receipt
