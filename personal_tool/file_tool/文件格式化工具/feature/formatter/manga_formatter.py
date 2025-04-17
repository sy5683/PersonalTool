import logging
import re

from ..file_feature import FileFeature
from ..image_feature import ImageFeature


class MangaFormatter:

    @staticmethod
    def format_manga_name(directory_path: pathlib.Path, start_number: int):
        """格式化漫画名称"""
        logging.info(f"格式化漫画名称: {directory_path.stem}")
        manga_paths = FileFeature.get_file_paths(directory_path)
        for index, manga_path in enumerate(manga_paths):
            number = str(start_number + index).zfill(max(len(str(len(manga_paths))), 3))
            # 1) 更改文件名
            new_manga_path = FileFeature.file_rename(manga_path, f"{number}{manga_path.suffix}")
            # 2) 处理webp文件
            if re.search(r"\.webp$", manga_path.suffix):
                ImageFeature.webp_to_jpg(new_manga_path)
        # 2) 收尾操作再次重命名文件，将temp去掉
        for path in FileFeature.get_file_paths(directory_path):
            FileFeature.file_rename(path)
