import abc

from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import ReceiptProfile
from ....entity.receipt_type import ReceiptType


class CCBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """建设银行回单格式"""

    def __init__(self, receipt_profile: ReceiptProfile):
        super().__init__("建设银行", receipt_profile)
