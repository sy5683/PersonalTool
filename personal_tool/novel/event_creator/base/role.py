from abc import ABCMeta, abstractmethod


class Role(metaclass=ABCMeta):
    """角色"""

    def __init__(self):
        # 角色基本信息
        self.name = None

        # 设置角色信息
        self.set_role_info()
        self.__check_role_inifo()

    @abstractmethod
    def set_role_info(self):
        """设置角色信息"""

    def __check_role_inifo(self):
        """校验角色信息"""
        assert self.name, f"角色类【{self.__class__.__name__}】名称未设置"
