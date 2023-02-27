import importlib
from pathlib import Path
from typing import List

from personal_tool.novel.event_creator.base.role import Role


class EntityFeature:
    _all_roles: List[Role] = None

    @classmethod
    def get_all_roles(cls):
        """获取所有角色"""
        if cls._all_roles is None:
            cls._all_roles = []
            cls.__import_entities("role")
            for role in Role.__subclasses__():
                cls._all_roles.append(role())
        return cls._all_roles

    @staticmethod
    def __import_entities(entity_type: str):
        """自动导入"""
        entity_dir_path = Path(__file__).parent.parent.joinpath(f"entity\\{entity_type}")
        for role_path in entity_dir_path.rglob("*.py"):
            module_name = f"personal_tool.novel.event_creator.entity.{entity_type}.{role_path.stem}"
            importlib.import_module(module_name)
