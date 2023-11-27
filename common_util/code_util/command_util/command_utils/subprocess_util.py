import subprocess
import sys


class SubprocessUtil:

    @classmethod
    def check_process_running(cls, process_name: str) -> bool:
        """判断程序是否运行"""
        result = cls._run_cmd_and_get_result(f'tasklist /fi "imagename eq {process_name}"')
        return process_name in result

    @classmethod
    def netstat_port(cls, port: int) -> bool:
        """判断端口是否正在运行"""
        if sys.platform == "win32":
            cmd = f'netstat -ano | findstr "{port}" | findstr "LISTEN"'
        else:
            cmd = f'netstat -ano | grep {port} | grep LISTEN'
        result = cls._run_cmd_and_get_result(cmd)
        return str(port) in result

    @staticmethod
    def _run_cmd_and_get_result(cmd: str) -> str:
        """运行cmd命令并获取结果"""

        with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, encoding='gbk') as p:
            return p.stdout.read()
