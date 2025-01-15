import abc

from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import TableProfile
from ....entity.receipt_type import ReceiptType


class YNRCCReceiptType(ReceiptType, metaclass=abc.ABCMeta):
    """云南农村信用社回单格式"""

    def __init__(self, profile: TableProfile):
        super().__init__("云南农村信用社", profile)
