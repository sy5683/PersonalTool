from .command_utils.cmd_util import CmdUtil
from .command_utils.subprocess_util import SubprocessUtil


class CommandUtil:

    @staticmethod
    def check_process_running(process_name: str) -> bool:
        """判断程序是否运行"""
        return SubprocessUtil.check_process_running(process_name)

    @staticmethod
    def pip_install(requirement_name: str, requirement_version: str = '', timeout: int = 120):
        """安装python依赖"""
        CmdUtil.pip_install(requirement_name, requirement_version, timeout)
