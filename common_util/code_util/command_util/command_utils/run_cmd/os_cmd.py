import logging
import os


class OsCmd:

    @staticmethod
    def install_python_package(requirement_name: str, requirement_version: str, timeout: int):
        """安装python库"""
        cmd_code = f"pip install --default-timeout={timeout}"
        cmd_code += " -i https://pypi.doubanio.com/simple"
        cmd_code += f" {requirement_name}"
        cmd_code += f"=={requirement_version}" if requirement_version else ""
        logging.info(f"cmd指令: {cmd_code}")
        os.system(cmd_code)
