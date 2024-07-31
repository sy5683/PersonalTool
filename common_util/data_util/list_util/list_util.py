import typing

from .list_utils.process_list import ProcessList


class ListUtil:

    @staticmethod
    def check_contain(big_list: list, small_list: list) -> list:
        """检查列表是否包含，返回缺失数据"""
        return ProcessList.check_contain(big_list, small_list)

    @staticmethod
    def cut_list(listing: list, cut_len: int) -> typing.List[list]:
        """列表切割"""
        return ProcessList.cut_list(listing, cut_len)

    @staticmethod
    def deduplicate(listing: list, sort: bool = False) -> list:
        """列表去重"""
        return ProcessList.deduplicate(listing, sort)

    @staticmethod
    def get_combinations(listing: list, max_len: int = 3) -> typing.List[tuple]:
        """获取列表排列组合"""
        return ProcessList.get_combinations(listing, max_len)
