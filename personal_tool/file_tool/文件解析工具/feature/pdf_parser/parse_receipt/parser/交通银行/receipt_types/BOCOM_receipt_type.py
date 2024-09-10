import abc

from ....entity.receipt_type import ReceiptType


class BOCOMReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """交通银行回单格式"""
