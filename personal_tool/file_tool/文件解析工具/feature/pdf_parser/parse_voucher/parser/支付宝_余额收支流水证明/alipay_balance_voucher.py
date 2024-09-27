from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .entity.revenue_statement import RevenueStatement
from ...entity.voucher_parser import VoucherParser


class AlipayBalanceVoucher(VoucherParser):

    def __init__(self, voucher_path: str, **kwargs):
        super().__init__("【支付宝】余额收支流水证明", voucher_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("余额收支流水证明")

    def parse(self):
        """解析"""
        try:
            table = self.pdf_profiles[0].tables[0]
        except IndexError:
            raise ValueError("无法在余额收支流水证明中提取出表格数据")
        tags = table.get_row_values(0)
        for row in range(1, table.max_rows):
            data = dict(zip(tags, table.get_row_values(row)))
            voucher = RevenueStatement()
            voucher.date = TimeUtil.format_to_str(data.get("入账时间"))
            voucher.transaction_number = data.get("支付宝交易号")
            voucher.merchant_order_number = data.get("商户订单号")
            voucher.business_type = data.get("业务类型")
            voucher.payee_account_name = data.get("对方账户名称")
            voucher.payee_account_number = data.get("对方支付宝账号/银行卡号")
            voucher.revenue_balance = NumberUtil.to_amount(data.get("收支余额"))
            voucher.account_balance = NumberUtil.to_amount(data.get("账户余额"))
            voucher.remarks = data.get("备注")
            self.vouchers.append(voucher)
