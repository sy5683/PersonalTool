import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .BOCOM_receipt_type import BOCOMReceiptType
from ....entity.receipt import Receipt


class BOCOMReceiptType01(BOCOMReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.max_rows != 1 or self.table.max_cols != 1:
            # 特殊格式，其生成了额外的小单元格包住了金额行
            if self.table.max_rows == 2 and self.table.max_cols == 7:
                return True
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        # 交通银行这个格式的回单数据全在一个大的表格单元格中，重新加载其为word数据后使用word方法解析
        self.words += PdfUtil.merge_words(self.table.cells[0].words, 20)
        receipt.date = TimeUtil.format_to_str(self._get_word("记账日期[:：](.*?)$"))  # 日期
        receipt.receipt_number = self._get_word("^回单编号[:：](.*?)(回单类型|$)")  # 回单编号
        receipt.serial_number = self._get_word("^会计流水号[:：](.*?)$")  # 流水号
        receipt.payer_account_name = self.__get_data("^付款人名称")  # 付款人户名
        receipt.payer_account_number = self.__get_data("^付款人账号")  # 付款人账号
        receipt.payer_account_bank = self.__get_data("^开户行名称", 0)  # 付款人开户银行
        receipt.payee_account_name = self.__get_data("^收款人名称")  # 收款人户名
        receipt.payee_account_number = self.__get_data("^收款人账号")  # 收款人账号
        receipt.payee_account_bank = self.__get_data("^开户行名称", 1)  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_word("金额[:：](.*?)$"))  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt

    def __get_data(self, pattern: str, index: int = 0) -> str:
        """获取回单数据"""
        # 这个格式的回单数据格式问题严重，经常会有值在键的上方的情况，因此这里实现方法单独处理，实现一个特殊的取数代码
        for _index, word in enumerate(self.words):
            # 如果取到了一个完全相等的数据，则说明数据坐标错位，需要取上一个word的值
            if re.search(f"{pattern}[:：]$", word.text):
                last_word = self.words[_index - 1].text
                if not re.search("[:：]", last_word):
                    return last_word  # 上一个word的值中必须没有冒号
        return self._get_words(f"{pattern}[:：](.*?)$")[index]
