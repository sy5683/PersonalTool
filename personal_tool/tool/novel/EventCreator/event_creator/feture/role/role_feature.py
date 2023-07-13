import random
from pathlib import Path
from typing import List

from .base.role_base import RoleBase
from ...util.import_util import ImportUtil


class RoleFeature:
    ImportUtil.import_module(Path(__file__).parent.joinpath("entity"))
    _all_roles: List[RoleBase] = None

    @classmethod
    def get_all_roles(cls) -> List[RoleBase]:
        """获取所有角色"""
        if cls._all_roles is None:
            cls._all_roles = [role() for role in RoleBase.__subclasses__()]
        return cls._all_roles

    @classmethod
    def get_random_roles(cls, partake_size: int = 1) -> List[RoleBase]:
        """随机选择列表中多个数据生成列表"""
        all_roles = cls.get_all_roles()
        return random.sample(all_roles, min(len(all_roles), random.randint(1, partake_size)))
