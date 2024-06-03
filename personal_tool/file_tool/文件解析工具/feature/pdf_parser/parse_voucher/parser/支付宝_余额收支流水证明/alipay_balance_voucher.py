import re

import fitz

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from ...entity.voucher import Voucher
from ...entity.voucher_parser import VoucherParser


class AlipayBalanceVoucher(VoucherParser):

    def __init__(self, voucher_path: str, **kwargs):
        super().__init__("【支付宝】余额收支流水证明", voucher_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        with fitz.open(self.voucher_path) as pdf:
            pdf_text = re.sub(r"\s+", "", pdf[0].get_text())
            if re.search("^支付宝", pdf_text) and "余额收支流水证明" in pdf_text:
                return True
        return False

    def parse(self):
        """解析"""
        try:
            table = self.pdf_profiles[0].tables[0]
        except IndexError:
            raise ValueError("无法在余额收支流水证明中提取出表格数据")
        tags = table.get_row_values(0)
        for row in range(1, table.max_rows):
            data = dict(zip(tags, table.get_row_values(row)))
            voucher = Voucher()
            voucher.date = TimeUtil.format_to_str(data.get("入账时间"))
            voucher.zfbjyh = data.get("支付宝交易号")
            voucher.shddh = data.get("商户订单号")
            voucher.ywlx = data.get("业务类型")
            voucher.dfzhmc = data.get("对方账户名称")
            voucher.dfzfbzh = data.get("对方支付宝账号/银行卡号")
            voucher.szye = NumberUtil.to_amount(data.get("收支余额"))
            voucher.zhye = NumberUtil.to_amount(data.get("账户余额"))
            voucher.bz = data.get("备注")
            self.vouchers.append(voucher)
