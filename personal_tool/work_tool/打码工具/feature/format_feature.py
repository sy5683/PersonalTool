from pathlib import pathlib.Path

from .enum.color_map import ColorMap


class FormatFeature:

    @staticmethod
    def format_coding(dir_path: pathlib.Path):
        """格式化打码内容"""
        for file_path in dir_path.glob("*.*"):
            coding: str = file_path.stem
            # 替换标注特殊情况（标注的中文需要使用【!】，但是因为按键麻烦，标注的时候使用的【,】代表中文，这里将其转换回来）
            coding = coding.replace(",", "!")
            # 将所有的标注内容统一改为大写
            coding = coding.upper()
            # 将标注内容中统一添加【_】，简化后续标注颜色的操作
            if "_" not in coding:
                coding += "_"
            # 跳过未变更的文件
            if coding == file_path.stem:
                continue
            file_path.rename(dir_path.joinpath(f"{coding}{file_path.suffix}"))

    @staticmethod
    def format_color(dir_path: pathlib.Path):
        """格式化颜色"""
        # 1) 格式化颜色之前需要先检测标识的颜色
        for file_path in dir_path.glob("*.*"):
            # 确保已标识了颜色并使用【_】隔开标注与颜色
            assert "_" in file_path.stem, f"打码文件有未标识出颜色的文件: {file_path.stem}"
            coding, color = file_path.stem.split("_")
            # 确保标注内容与颜色内容等长，没有出现标注错误的情况
            assert len(coding) == len(color), f"打码文件标识出的颜色不正确: {file_path.stem}"
            # 确保标注的颜色无论是颜色代码还是颜色内容，都在已有的颜色配置映射表中存在
            [ColorMap.code_to_name(code) for code in color]
        # 2) 将标识的颜色代码转换为目标颜色内容
        for file_path in dir_path.glob("*.*"):
            coding, color = file_path.stem.split("_")
            color_mapping = "".join([ColorMap.code_to_name(code) for code in color])
            file_path.rename(dir_path.joinpath(f"{coding}_{color_mapping}{file_path.suffix}"))
