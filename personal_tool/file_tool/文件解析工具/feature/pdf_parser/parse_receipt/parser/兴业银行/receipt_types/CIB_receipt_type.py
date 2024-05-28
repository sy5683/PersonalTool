import abc

from ....entity.receipt_type import ReceiptType


class CIBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """兴业银行回单格式"""
