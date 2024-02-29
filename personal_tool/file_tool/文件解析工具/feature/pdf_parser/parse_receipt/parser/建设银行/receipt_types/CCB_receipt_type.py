import abc

from ....entity.receipt_type import ReceiptType


class CCBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """建设银行回单格式"""
