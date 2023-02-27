import importlib
from pathlib import Path
from typing import List

from base.tool_base import ToolBase
from personal_tool.novel.event_creator.base.role import Role


class EventCreator(ToolBase):
    """事件生成器"""
    _all_roles: List[Role] = None

    def main(self):
        pass

    def _get_all_roles(self):
        """获取所有角色"""
        if self._all_roles is None:
            self._all_roles = []
            self.__import_entities("role")
            for role in Role.__subclasses__():
                self._all_roles.append(role())
        return self._all_roles

    @staticmethod
    def __import_entities(entity_type: str):
        """自动导入"""
        entity_dir_path = Path(__file__).parent.joinpath(f"entity\\{entity_type}")
        for role_path in entity_dir_path.rglob("*.py"):
            module_name = f"personal_tool.novel.event_creator.entity.{entity_type}.{role_path.stem}"
            importlib.import_module(module_name)
