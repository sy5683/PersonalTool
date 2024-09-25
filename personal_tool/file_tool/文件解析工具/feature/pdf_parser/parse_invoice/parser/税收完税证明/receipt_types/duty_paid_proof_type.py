import abc

from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import TableProfile
from ....entity.invoice_type import InvoiceType


class DutyPaidProofType(InvoiceType, metaclass=abc.ABCMeta):
    """税收完税证明格式"""

    def __init__(self, profile: TableProfile):
        super().__init__("税收完税证明", profile)
