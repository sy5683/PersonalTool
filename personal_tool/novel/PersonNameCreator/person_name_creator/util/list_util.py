class ListUtil:

    @staticmethod
    def list_de_duplicate(listing: list, sort: bool = False) -> list:
        """使用set转为集合实现列表去重"""
        de_duplicate_list = list(set(listing))
        if not sort:
            # set会重新排序列表，因此可以使用sort(.index)来保持原始顺序
            de_duplicate_list.sort(key=listing.index)
        return de_duplicate_list
