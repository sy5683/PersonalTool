import logging
import os
from pathlib import Path

from common_util.code_util.import_util.import_util import ImportUtil
from .entity.receipt_profile import ReceiptProfile


class ParseReceipt:
    ImportUtil.import_modules(Path(__file__).parent.joinpath("profiles"))

    @staticmethod
    def parse_receipt(receipt_path: str, **kwargs) -> ReceiptProfile:
        """解析银行回单"""
        logging.info(f"解析解析银行回单: {receipt_path}")
        receipt_name = os.path.basename(receipt_path)
        profiles = []
        for profile_class in ReceiptProfile.__subclasses__():
            profile = profile_class(receipt_path=receipt_path, **kwargs)
            if profile.judge():
                profiles.append(profile)
        if not len(profiles):
            raise ValueError(f"银行回单【{receipt_name}】无法识别")
        elif len(profiles) > 1:
            raise ValueError(
                f"银行回单【{receipt_name}】匹配多种格式: %s" % "、".join([each.bank_name for each in profiles]))
        else:
            receipt_profile = profiles[0]
            logging.info(f"银行回单【{receipt_name}】的类型为: {receipt_profile.bank_name}回单")
            receipt_profile.parse_receipt()  # 调用解析回单方法
            return receipt_profile
