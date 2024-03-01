import abc

from ....entity.receipt_type import ReceiptType


class BOCReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """中国银行回单格式"""
