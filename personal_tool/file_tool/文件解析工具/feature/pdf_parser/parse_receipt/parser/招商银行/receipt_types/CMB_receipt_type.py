import abc

from ....entity.receipt_type import ReceiptType


class CMBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """招商银行回单格式"""
