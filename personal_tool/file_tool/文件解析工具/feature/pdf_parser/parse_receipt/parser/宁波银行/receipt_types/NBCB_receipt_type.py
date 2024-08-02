import abc

from ....entity.receipt_type import ReceiptType


class NBCBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """宁波银行回单格式"""
