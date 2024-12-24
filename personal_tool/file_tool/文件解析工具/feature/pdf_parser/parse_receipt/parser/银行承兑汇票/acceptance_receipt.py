import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .entity.acceptance import Acceptance
from ...entity.receipt_parser import ReceiptParser


class AcceptanceReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        kwargs['threshold_x'] = 25
        super().__init__("银行承兑汇票", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("渤海银行电子印图案", "电子银行承兑汇票")

    def parse(self):
        """解析"""
        try:
            # 申报表页面只有第一张，后面的附表不需要解析
            profile = self.pdf_profiles[0]
            # 申报表只有一个表格，其余的无需处理
            table = profile.tables[0]
            words = profile.words
        except IndexError:
            raise ValueError("无法在电子银行承兑汇票中提取出表格数据")
        acceptance = Acceptance()
        acceptance.date = TimeUtil.format_to_str(PdfUtil.filter_word(words, "^出票日期[:：](.*?)$"))  # 日期
        acceptance.receipt_number = PdfUtil.filter_word(words, "^票据号码[:：](.*?)$")  # 回单编号
        acceptance.due_date = TimeUtil.format_to_str(
            PdfUtil.filter_word(words, "^(汇票到期日|汇票到日期)[:：](.*?)$"))  # 汇票到期日
        name_row_cells = table.get_row_cells(0)
        number_row_cells = table.get_row_cells(1)
        bank_row_cells = table.get_row_cells(2)
        if re.search("出票人", name_row_cells[0].get_value()):
            acceptance.payer_account_name = name_row_cells[2].get_value()  # 付款人户名
            acceptance.payer_account_number = number_row_cells[1].get_value()  # 付款人账号
            acceptance.payer_account_bank = bank_row_cells[1].get_value()  # 付款人开户银行
            acceptance.payee_account_name = name_row_cells[5].get_value()  # 收款人户名
            acceptance.payee_account_number = number_row_cells[3].get_value()  # 收款人账号
            acceptance.payee_account_bank = bank_row_cells[3].get_value()  # 收款人开户银行
        elif re.search("收款人", name_row_cells[0].get_value()):
            acceptance.payer_account_name = name_row_cells[5].get_value()  # 付款人户名
            acceptance.payer_account_number = number_row_cells[3].get_value()  # 付款人账号
            acceptance.payer_account_bank = bank_row_cells[3].get_value()  # 付款人开户银行
            acceptance.payee_account_name = name_row_cells[2].get_value()  # 收款人户名
            acceptance.payee_account_number = number_row_cells[1].get_value()  # 收款人账号
            acceptance.payee_account_bank = bank_row_cells[1].get_value()  # 收款人开户银行
        # 承兑人信息$
        acceptor_cell = table.get_cell_relative("^承兑人信息$", 0)
        acceptor_row_cells_1 = table.get_row_cells(acceptor_cell.row)
        acceptor_row_cells_2 = table.get_row_cells(acceptor_cell.row + 1)
        acceptance.acceptor_account_name = acceptor_row_cells_1[2].get_value()  # 承兑人全称
        acceptance.acceptor_account_number = acceptor_row_cells_1[4].get_value()  # 承兑人账号
        acceptance.acceptor_account_bank_name = acceptor_row_cells_2[3].get_value()  # 承兑人开户银行名称
        acceptance.acceptor_account_bank_number = acceptor_row_cells_2[1].get_value()  # 承兑人开户银行行号
        # 根据承兑人开户银行名称判断票据所属银行，再根据所属银行取出金额
        amount_cell = table.get_cell_relative("^票据金额", 0)
        if re.search("渤海银行", acceptance.acceptor_account_bank_name):
            acceptance.acceptor_bank = "渤海银行"  # 承兑所属银行
            amount = "".join([each.get_value() for each in table.get_row_cells(amount_cell.row + 1)])
            acceptance.amount = NumberUtil.to_amount(amount)  # 金额
        elif re.search("农业银行", acceptance.acceptor_account_bank_name):
            acceptance.acceptor_bank = "农业银行"  # 承兑所属银行
            acceptance.amount = NumberUtil.to_amount(table.get_row_cells(amount_cell.row)[-1].get_value())  # 金额
        self.receipts.append(acceptance)
