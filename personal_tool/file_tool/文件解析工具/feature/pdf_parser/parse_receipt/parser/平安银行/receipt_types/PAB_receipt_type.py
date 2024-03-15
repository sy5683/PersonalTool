import abc

from ....entity.receipt_type import ReceiptType


class PABReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """平安银行回单格式"""
