import os.path
import shutil
import tempfile
from pathlib import Path

import win32api


class PackTool:

    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        assert self.tool_name, "工具名称不能为空"
        self.save_path = tempfile.mkdtemp()

    def __del__(self):
        win32api.ShellExecute(0, "open", self.save_path, "", "", 1)

    def copy_tool(self):
        """复制工具"""
        # 1) 复制工具
        copy_tool_path = os.path.join(self.save_path, self.tool_name)
        shutil.copytree(self._get_tool_path(), copy_tool_path)
        # 2) 复制框架
        core_path = self.__to_project_path("common_core")
        copy_core_path = os.path.join(self.save_path, f"{self.tool_name}\\{core_path.name}")
        shutil.copytree(core_path, copy_core_path)
        # 3) 复制组件
        util_path = self.__to_project_path("common_util")
        copy_util_path = os.path.join(self.save_path, f"{self.tool_name}\\{util_path.name}")
        shutil.copytree(util_path, copy_util_path)

    def _get_tool_path(self) -> Path:
        """获取工具路径"""
        # 1) 获取工具路径
        tool_dir_path = self.__to_project_path("personal_tool")
        try:
            tool_path = next(tool_dir_path.rglob(self.tool_name))
        except StopIteration:
            raise Exception(f"未找到目标工具文件: {self.tool_name}")
        # 2) 校验获取到的路径
        # 2.1) 根据命名规则，工具根目录同级不能有py文件
        if list(tool_path.parent.glob("*.py")):
            raise Exception(f"文件路径异常，并不为工具根目录: {tool_path}")
        # 2.2) 根据命名规则，工具根目录子级不能没有py文件
        if not list(tool_path.glob("*.py")):
            raise Exception(f"文件路径异常，并不为工具根目录: {tool_path}")
        return tool_path

    @staticmethod
    def __to_project_path(file_name: str = '') -> Path:
        """获取项目路径"""
        return Path(__file__).parent.parent.joinpath(file_name)


if __name__ == '__main__':
    PackTool("表头转换工厂").copy_tool()
