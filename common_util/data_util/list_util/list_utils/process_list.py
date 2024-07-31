import itertools
import typing


class ProcessList:

    @staticmethod
    def check_contain(big_list: list, small_list: list) -> list:
        """检查列表是否包含，返回缺失数据"""
        return [small for small in small_list if small not in big_list]

    @staticmethod
    def cut_list(listing: list, cut_len: int) -> typing.List[list]:
        """列表切割"""
        return [listing[index:index + cut_len] for index in range(0, len(listing), cut_len)]

    @staticmethod
    def duplicate_remove(listing: list, sort: bool) -> list:
        """列表去重"""
        duplicate_listing = list(set(listing))
        if not sort:
            # set会重新排序列表，可以使用sort(.index)来保持原始顺序
            duplicate_listing.sort(key=listing.index)
        return duplicate_listing

    @staticmethod
    def get_combinations(listing: list, max_len: int) -> typing.List[tuple]:
        """获取列表排列组合"""
        combinations = []
        for length in range(1, min(len(listing), max_len) + 1):
            for combination in itertools.combinations(listing, length):
                combinations.append(combination)
        return combinations
