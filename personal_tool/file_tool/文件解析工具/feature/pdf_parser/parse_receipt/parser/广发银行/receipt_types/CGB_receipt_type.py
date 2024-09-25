import abc

from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import TableProfile
from ....entity.receipt_type import ReceiptType


class CGBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """广发银行回单格式"""

    def __init__(self, profile: TableProfile):
        super().__init__("广发银行", profile)
