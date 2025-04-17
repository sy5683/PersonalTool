import os
import platform

from .enum.system_type import SystemType


class SystemInfo:

    @staticmethod
    def get_system_type() -> SystemType:
        """获取系统类型"""
        if os.name == "nt":
            return SystemType.Windows
        elif os.name == "posix":
            if "KYLIN" in platform.version().upper():
                return SystemType.Kylin
            return SystemType.UOS
        return SystemType.unknown
