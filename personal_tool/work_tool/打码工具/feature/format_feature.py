from pathlib import Path


class FormatFeature:

    @staticmethod
    def format_coding(dir_path: Path):
        """格式化打码内容"""
        for file_path in dir_path.glob("*.*"):
            coding: str = file_path.stem
            coding = coding.replace(",", "!")
            coding = coding.upper()
            if "_" not in coding:
                coding += "_"
            if coding == file_path.stem:
                continue
            file_path.rename(dir_path.joinpath(f"{coding}{file_path.suffix}"))

    @staticmethod
    def format_color(dir_path: Path):
        """格式化颜色"""
        for file_path in dir_path.glob("*.*"):
            assert "_" in file_path.stem, f"打码文件有未标识出颜色的文件: {file_path}"
        for file_path in dir_path.glob("*.*"):
            code, color = file_path.stem.split("_")
            print([code, color])
