import abc

from ....entity.receipt_type import ReceiptType


class PSBCReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """邮储银行回单格式"""
