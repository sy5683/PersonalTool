import itertools
import typing


class ProcessList:

    @staticmethod
    def get_combinations(listing: list, max_len: int) -> typing.List[tuple]:
        """获取列表排列组合"""
        combinations = []
        for length in range(1, min(len(listing), max_len) + 1):
            for combination in itertools.combinations(listing, length):
                combinations.append(combination)
        return combinations
