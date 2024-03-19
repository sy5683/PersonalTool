import abc

from ....entity.receipt_type import ReceiptType


class CDBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """国开行回单格式"""
