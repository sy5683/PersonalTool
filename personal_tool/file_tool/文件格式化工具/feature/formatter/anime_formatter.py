import logging
import re
from pathlib import Path

from ..file_feature import FileFeature


class AnimeFormatter:

    @staticmethod
    def format_anime_name(directory_path: Path, anime_name: str = None):
        """格式化动漫名称"""
        # 未指定动漫名称则取文件夹名称
        if anime_name is None:
            anime_name = directory_path.stem
        logging.info(f"格式化动漫名称: {anime_name}")
        for index, anime_path in enumerate(FileFeature.get_file_paths(directory_path)):
            # 1) 更改文件名
            episodes = str(index + 1).zfill(2)
            title = re.findall("「(.*?)」", anime_path.stem)
            new_anime_name = f"{anime_name} [{episodes}] 「{title[0] if title else ''}」{anime_path.suffix}"
            FileFeature.file_rename(anime_path, new_anime_name)
        # 2) 收尾操作再次重命名文件，将temp去掉
        for path in FileFeature.get_file_paths(directory_path):
            FileFeature.file_rename(path)
