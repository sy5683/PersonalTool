import abc

from ....entity.receipt_type import ReceiptType


class CEXIMReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """中国进出口银行回单格式"""
