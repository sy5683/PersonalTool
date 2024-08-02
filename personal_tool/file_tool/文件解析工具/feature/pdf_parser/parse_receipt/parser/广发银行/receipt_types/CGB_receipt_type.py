import abc

from ....entity.receipt_type import ReceiptType


class CGBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """广发银行回单格式"""
