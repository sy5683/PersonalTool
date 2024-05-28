import abc

from ....entity.receipt_type import ReceiptType


class FCReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """财务公司回单格式"""
