import os


class CmdUtil:

    @staticmethod
    def pip_install(requirement_name: str, requirement_version: str, timeout: int):
        """安装python依赖"""
        cmd_code = f"pip install --default-timeout={timeout}"
        cmd_code += " -i https://pypi.tuna.tsinghua.edu.cn/simple"
        cmd_code += f" {requirement_name}"
        cmd_code += f"=={requirement_version}" if requirement_version else ""
        os.system(cmd_code)
