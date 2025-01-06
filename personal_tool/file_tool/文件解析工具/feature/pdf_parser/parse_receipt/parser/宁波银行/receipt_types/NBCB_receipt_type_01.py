import re

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
        receipt.serial_number = self.table.get_cell(5, 3).get_value()  # 流水号
        receipt.date = TimeUtil.format_to_str(self._get_word("^.*年.*月.*日$"))  # 日期
        business_type = self.table.get_cell(5, 1).get_value()  # 业务种类
        # TODO 根据业务种类判断收付款类型，判断逻辑待定
        # 备注信息
        remarks = self.table.get_cell(6, 1).get_value("\t").replace("：", ":")
        payer_account_name_pattern = re.compile("付款人户名[:：]")
        payer_account_number_pattern = re.compile("付款人账号[:：]")
        payer_account_bank_pattern = re.compile("付款行行名[:：]")
        payee_account_name_pattern = re.compile("收款人户名[:：]")
        payee_account_number_pattern = re.compile("收款人账号[:：]")
        payee_account_bank_pattern = re.compile("收款行行名[:：]")
        for remark in re.split(r"\s+", remarks):
            if payer_account_name_pattern.search(remark):
                receipt.payer_account_name = payer_account_name_pattern.sub("", remark)  # 付款人户名
            if payer_account_number_pattern.search(remark):
                receipt.payer_account_number = payer_account_number_pattern.sub("", remark)  # 付款人账号
            if payer_account_bank_pattern.search(remark):
                receipt.payer_account_bank = payer_account_bank_pattern.sub("", remark)  # 付款人开户银行
            if payee_account_name_pattern.search(remark):
                receipt.payee_account_name = payee_account_name_pattern.sub("", remark)  # 收款人户名
            if payee_account_number_pattern.search(remark):
                receipt.payee_account_number = payee_account_number_pattern.sub("", remark)  # 收款人账号
            if payee_account_bank_pattern.search(remark):
                receipt.payee_account_bank = payee_account_bank_pattern.sub("", remark)  # 收款人开户银行
        amount = self.table.get_cell(3, 1).get_value()
        receipt.amount = NumberUtil.to_amount(amount.split("RMB")[-1] if "RMB" in amount else amount)  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt
