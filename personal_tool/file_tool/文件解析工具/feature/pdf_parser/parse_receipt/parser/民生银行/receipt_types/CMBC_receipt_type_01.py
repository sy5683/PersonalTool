from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .CMBC_receipt_type import CMBCReceiptType
from ....entity.receipt import Receipt


class CMBCReceiptType01(CMBCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not self._get_word("^支付业务回单[(（]收款[)）]$"):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.bank = self.bank_name  # 银行
        # 民生银行这个格式的回单间隔稍微大一点，重新合并word数据后再解析
        self.words = PdfUtil.merge_words(self.words, 30)
        receipt.date = TimeUtil.format_to_str(self._get_word("^交易日期[:：](.*?)(借|$)"))  # 日期
        receipt.serial_number = self._get_word("^交易流水号[:：](.*?)$")  # 流水号
        receipt.payer_account_name = self._get_word("^付款人名称[:：](.*?)$")  # 付款人户名
        receipt.payer_account_number = self._get_word("^付款人账号[:：](.*?)$")  # 付款人账号
        receipt.payee_account_name = self._get_word("^收款人名称[:：](.*?)$")  # 收款人户名
        receipt.payee_account_number = self._get_word("^收款人账号[:：](.*?)$")  # 收款人账号
        # 收款人开户行与付款人开户行的值过高，导致无法使用通用方式定位
        receipt.payer_account_bank = None  # 付款人开户银行
        receipt.payee_account_bank = None  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_word("^[(（]小写[)）](.*?)$"))  # 金额
        return receipt
