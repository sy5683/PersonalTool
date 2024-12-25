import re
import typing


class Receipt:

    def __init__(self):
        self.bank = None  # 银行
        self.date = None  # 日期
        self.receipt_number = None  # 回单编号
        self.serial_number = None  # 流水号
        self.payer_account_name = None  # 付款人户名
        self.payer_account_number = None  # 付款人账号
        self.payer_account_bank = None  # 付款人开户银行
        self.payee_account_name = None  # 收款人户名
        self.payee_account_number = None  # 收款人账号
        self.payee_account_bank = None  # 收款人开户银行
        self.amount = 0  # 金额
        self.image = None  # 图片

    def to_dict(self, with_image: bool = True) -> typing.Dict[str, str]:
        return {
            'bank': self.bank,
            'pay_bank': self.payer_account_bank,
            'pay_name': self.payer_account_name,
            'pay_no': self.payer_account_number,
            'account_bank': self.payee_account_bank,
            'account_name': self.payee_account_name,
            'account_no': self.payee_account_number,
            'date': self.date,
            'business_no': re.sub(r"\D", "", str(self.receipt_number)),
            'amount': self.amount,
            # 'use':self.receipt_value(receipt, '用途', '收费种类:', '附言:')
            'image': self.image if with_image else None  # 测试时为了便于查看，这里添加一个参数来控制显不显示image
        }
