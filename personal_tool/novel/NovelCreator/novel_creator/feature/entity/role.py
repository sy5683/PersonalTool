import logging
from abc import ABCMeta, abstractmethod


class Role(metaclass=ABCMeta):
    """角色"""

    def __init__(self, role_name: str = ''):
        self.role_name = role_name  # 角色名字
        self.persona = None  # 人设

        # 设置角色信息
        self.set_role_info()
        self.__check_role_info()

    @abstractmethod
    def set_role_info(self):
        """设置角色信息"""

    def __check_role_info(self):
        """校验角色信息"""
        assert self.role_name, f"角色类【{self.__class__.__name__}】名称未设置"
        if not self.persona:
            logging.warning(f"角色【{self.role_name}】人设未设置或待定")
