import abc

from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import TableProfile
from ....entity.receipt_type import ReceiptType


class PSBCReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """邮储银行回单格式"""

    def __init__(self, profile: TableProfile):
        super().__init__("邮储银行", profile)
