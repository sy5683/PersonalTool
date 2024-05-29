from ...entity.voucher_parser import VoucherParser


class WechatMerchantVoucher(VoucherParser):

    def __init__(self, voucher_path: str, **kwargs):
        super().__init__("【微信】商户结算记录", voucher_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""

    def parse_voucher(self):
        """解析凭证"""
