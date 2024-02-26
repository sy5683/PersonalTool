from ...entity.receipt_profile import ReceiptProfile


class ABC01Receipt(ReceiptProfile):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("农业银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return False

    def parse_receipt(self):
        """解析回单"""
