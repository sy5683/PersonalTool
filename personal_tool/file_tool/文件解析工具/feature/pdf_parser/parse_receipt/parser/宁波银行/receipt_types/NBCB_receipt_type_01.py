import re
import typing

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .NBCB_receipt_type import NBCBReceiptType
from ....entity.receipt import Receipt


class NBCBReceiptType01(NBCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if {"账号", "户名", "开户银行", "交易金额", "回单种类", "业务种类"} < set(self.table.get_col_values(0)):
            return True
        return False

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        receipt.serial_number = self._get_cell_relative("交易流水").get_value()  # 流水号
        receipt.date = TimeUtil.format_to_str(self._get_word("^.*年.*月.*日$"))  # 日期
        # 从备注信息里提取用户信息
        for remark in re.split(r"\s+", self.table.get_cell(6, 1).get_value("\t")):
            receipt.payer_account_name = self.get_remark_value("^付款人户名[:：]", remark)  # 付款人户名
            receipt.payer_account_number = self.get_remark_value("^付款人账号[:：]", remark)  # 付款人账号
            receipt.payer_account_bank = self.get_remark_value("^付款行行名[:：]", remark)  # 付款人开户银行
            receipt.payee_account_name = self.get_remark_value("^收款人户名[:：]", remark)  # 收款人户名
            receipt.payee_account_number = self.get_remark_value("^收款人账号[:：]", remark)  # 收款人账号
            receipt.payee_account_bank = self.get_remark_value("^收款行行名[:：]", remark)  # 收款人开户银行
        # 根据回单种类判断收付类型
        receipt_type = self._get_cell_relative("回单种类").get_value()
        # 付款回单: 转账支取回单
        if re.search("支取", receipt_type):
            receipt.payer_account_name = self._get_cell_relative("账号").get_value()  # 付款人户名
            receipt.payer_account_number = self._get_cell_relative("户名").get_value()  # 付款人账号
            receipt.payer_account_bank = self._get_cell_relative("开户银行").get_value()  # 付款人开户银行
        # 收款回单: 转账存入回单
        elif re.search("存入", receipt_type):
            receipt.payee_account_name = self._get_cell_relative("账号").get_value()  # 收款人户名
            receipt.payee_account_number = self._get_cell_relative("户名").get_value()  # 收款人账号
            receipt.payee_account_bank = self._get_cell_relative("开户银行").get_value()  # 收款人开户银行
        else:
            raise TypeError(f"宁波银行无法判断的回单种类，请联系开发增加解析格式: {receipt_type}")
        amount = self.table.get_cell(3, 1).get_value()
        receipt.amount = NumberUtil.to_amount(amount.split("RMB")[-1] if "RMB" in amount else amount)  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt

    @staticmethod
    def get_remark_value(pattern: str, value: str) -> typing.Union[str, None]:
        if re.search(pattern, value):
            return re.sub(pattern, "", value)
