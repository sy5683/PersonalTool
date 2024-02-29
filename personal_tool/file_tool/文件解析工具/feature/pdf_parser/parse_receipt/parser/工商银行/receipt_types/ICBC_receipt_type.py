import abc

from ....entity.receipt_type import ReceiptType


class ICBCReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """工商银行回单格式"""
