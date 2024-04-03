import typing

from .list_utils.process_list import ProcessList


class ListUtil:

    @staticmethod
    def get_combinations(listing: list, max_len: int = 3) -> typing.List[tuple]:
        """获取列表排列组合"""
        return ProcessList.get_combinations(listing, max_len)
