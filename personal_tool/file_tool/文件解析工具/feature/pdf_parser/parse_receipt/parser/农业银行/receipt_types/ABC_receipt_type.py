import abc

from ....entity.receipt_type import ReceiptType


class ABCReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """农业银行回单格式"""
