from .command_utils.run_cmd.os_cmd import OsCmd
from .command_utils.run_cmd.subprocess_cmd import SubprocessCmd


class CommandUtil:

    @staticmethod
    def check_process_running(process_name: str) -> bool:
        """判断程序是否正在运行"""
        return SubprocessCmd.check_process_running(process_name)

    @staticmethod
    def install_python_package(requirement_name: str, requirement_version: str = '', timeout: int = 120):
        """安装python库"""
        OsCmd.install_python_package(requirement_name, requirement_version, timeout)
