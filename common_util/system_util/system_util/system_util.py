from .system_utils.enum.system_type import SystemType
from .system_utils.system_info import SystemInfo


class SystemUtil:

    @staticmethod
    def get_system_type() -> SystemType:
        """获取系统类型"""
        return SystemInfo.get_system_type()
