from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .SCRCB_receipt_type import SCRCBReceiptType
from ....entity.receipt import Receipt


class SCRCBReceiptType01(SCRCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.max_cols == 1 and self.table.max_rows == 2:
            return True
        return False

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        # 四川农村商业银行这个格式的回单数据全在两个个大的表格单元格中，重新加载其为word数据后使用word方法解析
        for cell in self.table.cells:
            self.words += PdfUtil.merge_words(cell.words, 10)
        receipt.date = TimeUtil.format_to_str(self._get_word("^交易时间[:：](.*?)$"))  # 日期
        receipt.receipt_number = self._get_word("^电子回单号码[:：](.*?)$")  # 回单编号
        receipt.serial_number = self._get_word("^交易流水号[:：](.*?)$")  # 流水号
        receipt.payer_account_name = self._get_word("^(付款户名|户名)[:：](.*?)$")  # 付款人户名
        receipt.payer_account_number = self._get_word("^(付款账号|交易账号|扣费账号)[:：](.*?)$")  # 付款人账号
        receipt.payer_account_bank = "攀枝花农村商业银行股份有限公司"  # 付款人开户银行
        receipt.payee_account_name = self._get_word("^对方户名[:：](.*?)$")  # 收款人户名
        receipt.payee_account_number = self._get_word("^对方账号[:：](.*?)$")  # 收款人账号
        receipt.payee_account_bank = "攀枝花农村商业银行股份有限公司"  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_word("^交易金额[(（]小写[)）][:：](.*?)$"))  # 金额
        receipt.abstract = self._get_word("^摘要[:：](.*?)$")  # 摘要
        receipt.image = self.image  # 图片
        return receipt
