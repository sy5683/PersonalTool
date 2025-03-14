import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import TableProfile
from .entity.acceptance import Acceptance
from ...entity.receipt_parser import ReceiptParser


class AcceptanceReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        kwargs['threshold_x'] = 25
        super().__init__("银行承兑汇票", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not self._check_contains("电子银行承兑汇票"):
            return False
        # 有些回单中【凭证种类】的值为"电子银行承兑汇票"，会导致识别错误，因此这里再加一个承兑汇票的特殊值进行判断
        if not self._check_contains("承兑信息"):
            return False
        return True

    def parse(self):
        """解析"""
        try:
            # 申报表页面只有第一张，后面的附表不需要解析
            pdf_profile = self.pdf_profiles[0]
            # 申报表只有一个表格，其余的无需处理
            profile = TableProfile(pdf_profile.tables[0], pdf_profile.words)
        except IndexError:
            raise ValueError("无法在电子银行承兑汇票中提取出表格数据")
        acceptance = Acceptance()
        acceptance.date = TimeUtil.format_to_str(PdfUtil.filter_word(profile.words, "^出票日期[:：](.*?)$"))  # 日期
        acceptance.receipt_number = PdfUtil.filter_word(profile.words, "^票据号码[:：](.*?)$")  # 回单编号
        acceptance.due_date = TimeUtil.format_to_str(
            PdfUtil.filter_word(profile.words, "^(汇票到期日|汇票到日期)[:：](.*?)$"))  # 汇票到期日
        name_row_cells = profile.table.get_row_cells(0)
        number_row_cells = profile.table.get_row_cells(1)
        bank_row_cells = profile.table.get_row_cells(2)
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
        acceptor_cell = profile.table.get_cell_relative("^承兑人信息$", 0)
        acceptor_row_cells_1 = profile.table.get_row_cells(acceptor_cell.row)
        acceptor_row_cells_2 = profile.table.get_row_cells(acceptor_cell.row + 1)
        acceptance.acceptor_account_name = acceptor_row_cells_1[2].get_value()  # 承兑人全称
        acceptance.acceptor_account_number = acceptor_row_cells_1[4].get_value()  # 承兑人账号
        acceptance.acceptor_account_bank_name = acceptor_row_cells_2[3].get_value()  # 承兑人开户银行名称
        acceptance.acceptor_account_bank_number = acceptor_row_cells_2[1].get_value()  # 承兑人开户银行行号
        # 根据承兑人开户银行名称判断票据所属银行，再根据所属银行取出金额
        amount_cell = profile.table.get_cell_relative("^票据金额", 0)
        if re.search("渤海银行", acceptance.acceptor_account_bank_name):
            acceptance.bank = "渤海银行"  # 承兑所属银行
            amounts = [each.get_value() for each in profile.table.get_row_cells(amount_cell.row + 1)]
            amounts = amounts[:-2] + ["."] + amounts[-2:]  # 渤海银行金额没有小数点，取出的数据需要在角分之前加个小数点
            acceptance.amount = NumberUtil.to_amount("".join(amounts))  # 金额
        elif re.search("农业银行", acceptance.acceptor_account_bank_name):
            acceptance.bank = "农业银行"  # 承兑所属银行
            acceptance.amount = NumberUtil.to_amount(profile.table.get_row_cells(amount_cell.row)[-1].get_value())  # 金额
        acceptance.type = f"{acceptance.bank}{self.parser_type}"  # 类型
        acceptance.abstract = ""  # 摘要
        PdfUtil.split_pdf_image(profile, pdf_profile.image)
        acceptance.image = profile.image  # 图片
        self.receipts.append(acceptance)
        # 解析完成后对整张解析后的银行回单做收支类型等信息的提前和整合
        self._format_parser()
