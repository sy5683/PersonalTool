from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_utils.entity.pdf_element import Table
from .entity.settlement_record import SettlementRecord
from ...entity.voucher_parser import VoucherParser


class WechatMerchantVoucher(VoucherParser):

    def __init__(self, voucher_path: str, **kwargs):
        super().__init__("【微信】商户结算记录", voucher_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("商户结算记录")

    def parse(self):
        """解析"""
        try:
            table = self.pdf_profiles[0].tables[0]
        except IndexError:
            raise ValueError("无法在商户结算记录中提取出表格数据")
        tag_row = self.__get_tag_row(table)
        tags = table.get_row_values(tag_row)
        for row in range(tag_row + 1, table.max_rows):
            row_values = table.get_row_values(row)
            data = dict(zip(tags, row_values))
            voucher = SettlementRecord()
            voucher.date = TimeUtil.format_to_str(data.get("结算日期"))
            if not voucher.date:
                continue  # 跳过日期行不正确的数据（如：合计行）
            voucher.order_amount = NumberUtil.to_amount(data.get("订单金额(元)"))
            voucher.order_quantity = data.get("订单笔数")
            voucher.refund_amount = NumberUtil.to_amount(data.get("退款金额(元)"))
            voucher.refund_quantity = data.get("退款笔数")
            voucher.commission = NumberUtil.to_amount(data.get("手续费(元)"))
            voucher.entry_amount = NumberUtil.to_amount(data.get("入账金额(元)"))
            self.vouchers.append(voucher)

    @staticmethod
    def __get_tag_row(table: Table) -> int:
        """获取表头行"""
        for row in range(table.max_rows):
            row_values = table.get_row_values(row)
            if "结算日期" in row_values and "入账金额(元)" in row_values:
                return row
        raise ValueError("无法识别出表格表头")
