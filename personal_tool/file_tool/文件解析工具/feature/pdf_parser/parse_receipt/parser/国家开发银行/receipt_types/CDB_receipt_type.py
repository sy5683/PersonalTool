import abc

from ....entity.receipt_type import ReceiptType


class CDBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """国家开发银行回单格式"""
