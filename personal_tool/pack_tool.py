import os
import re
import shutil
import tempfile
import typing
from pathlib import Path

from common_util.code_util.win32_util.win32_util import Win32Util
from common_util.file_util.file_util.file_util import FileUtil


class PackTool:

    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        assert self.tool_name, "工具名称不能为空"
        self.copy_path = None

    def copy_tool(self):
        """复制工具"""
        # 1) 复制工具
        tool_path = self._get_tool_path()
        shutil.copytree(tool_path, self.__to_copy_path(self.tool_name))
        # 2) 复制框架
        core_path = self.__to_project_path("common_core")
        shutil.copytree(core_path, self.__to_copy_path(f"{self.tool_name}\\common_core"))
        # 3) 复制组件
        for relative_util_path in self._get_relative_util_paths(tool_path):
            util_path = self.__to_project_path(relative_util_path)
            copy_util_path = self.__to_copy_path(f"{self.tool_name}\\{relative_util_path}")
            shutil.copytree(util_path, copy_util_path)
        # 4) 删除一些无用文件
        for file_name in ["__pycache__"]:
            for file_path in Path(self.__to_copy_path()).rglob(file_name):
                FileUtil.delete_file(file_path)
        Win32Util.open_file(self.__to_copy_path())

    def _get_tool_path(self) -> Path:
        """获取工具路径"""
        # 1) 获取工具路径
        tool_dir_path = self.__to_project_path("personal_tool")
        try:
            tool_path = next(tool_dir_path.rglob(self.tool_name))
        except StopIteration:
            raise FileExistsError(f"未找到目标工具文件: {self.tool_name}")
        # 2) 校验获取到的路径。根据命名规则，工具根目录同级不能有py文件，子级不能没有py文件
        if list(tool_path.parent.glob("*.py")) or not list(tool_path.glob("*.py")):
            raise FileExistsError(f"文件路径异常，并不为工具根目录: {tool_path}")
        return tool_path

    @staticmethod
    def _get_relative_util_paths(tool_path: Path) -> typing.List[str]:
        """获取公共组件相对导入路径"""
        relative_util_paths = []
        for tool_py_path in tool_path.rglob("*.py"):
            with open(tool_py_path, "rb") as file:
                for line in file.readlines():
                    code = line.decode('utf-8')
                    if "import" not in code:
                        continue
                    module_path = re.findall(r"^from common_util\.(.*?)_util.? import", code)
                    if not module_path:
                        continue
                    relative_util_path = "\\".join(["common_util"] + module_path[0].split(".")[:-1])
                    if relative_util_path not in relative_util_paths:
                        relative_util_paths.append(relative_util_path)
        return relative_util_paths

    @staticmethod
    def __to_project_path(file_name: str = '') -> Path:
        """获取项目路径"""
        return Path(__file__).parent.parent.joinpath(file_name)

    def __to_copy_path(self, file_name: str = '') -> str:
        if self.copy_path is None:
            self.copy_path = tempfile.mkdtemp()
        return os.path.join(self.copy_path, file_name)


if __name__ == '__main__':
    PackTool("国税系统脚本").copy_tool()
