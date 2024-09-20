import abc

from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import ReceiptProfile
from ....entity.receipt_type import ReceiptType


class CMBReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """招商银行回单格式"""

    def __init__(self, receipt_profile: ReceiptProfile):
        super().__init__("招商银行", receipt_profile)
