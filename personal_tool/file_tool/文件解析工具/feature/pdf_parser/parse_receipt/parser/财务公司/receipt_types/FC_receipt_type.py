import abc

from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import ReceiptProfile
from ....entity.receipt_type import ReceiptType


class FCReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """财务公司回单格式"""

    def __init__(self, receipt_profile: ReceiptProfile):
        super().__init__("财务公司", receipt_profile)
