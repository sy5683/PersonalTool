import abc

from ....entity.receipt_type import ReceiptType


class SPDBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """浦发银行回单格式"""
