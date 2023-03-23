import importlib
import os
from pathlib import Path
from typing import List

from personal_tool.novel.event_creator.base.event import Event
from personal_tool.novel.event_creator.base.role import Role


class EntityFeature:
    _all_roles: List[Role] = None
    _all_events: List[Event] = None

    @staticmethod
    def import_entities():
        """自动导入实例"""
        entity_dir_path = Path(__file__).parent.parent.joinpath("entity")
        for role_path in entity_dir_path.rglob("*.py"):
            role_parts = role_path.parts
            for i in range(1, len(role_parts)):
                try:
                    module_name = ".".join(role_parts[i:])
                    importlib.import_module(os.path.splitext(module_name)[0])  # 一定要记得去除导入路径的后缀
                    break
                except ModuleNotFoundError:
                    pass

    @classmethod
    def get_all_roles(cls):
        """获取所有角色"""
        if cls._all_roles is None:
            cls._all_roles = [role() for role in Role.__subclasses__()]
        return cls._all_roles

    @classmethod
    def get_all_events(cls):
        """获取所有事件"""
        if cls._all_events is None:
            cls._all_events = [event() for event in Event.__subclasses__()]
        return cls._all_events
