import abc

from ....entity.receipt_type import ReceiptType


class CBHBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """渤海银行回单格式"""
