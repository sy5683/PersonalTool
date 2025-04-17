import abc
import logging
import sys


class Role(metaclass=abc.ABCMeta):
    """角色"""

    def __init__(self):
        __role_path = pathlib.Path(sys.modules[self.__module__].__file__)
        self.role_name = __role_path.stem  # 角色名字
        self.persona = """"""  # 人设

        # 设置角色信息
        self.set_role_info()
        self.__check_role_info()

    @abc.abstractmethod
    def set_role_info(self):
        """设置角色信息"""

    def __check_role_info(self):
        """校验角色信息"""
        if not self.persona:
            logging.warning(f"角色【{self.role_name}】人设未设置或待定")
