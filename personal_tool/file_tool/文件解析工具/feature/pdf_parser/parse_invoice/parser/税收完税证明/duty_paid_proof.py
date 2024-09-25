from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.duty_paid_proof_type import DutyPaidProofType
from ...entity.invoice_parser import InvoiceParser


class DutyPaidProof(InvoiceParser):

    def __init__(self, voucher_path: str, **kwargs):
        kwargs['threshold_x'] = 15
        super().__init__("税收完税证明", voucher_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("填票人电子税务局")

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for profile in PdfUtil.split_pdf(pdf_profile):
                self._parse_invoice(profile, DutyPaidProofType)
