import os.path
import os.path
import re
from pathlib import Path

from ..cache.path_cache import PathCache


class FormatFeature:

    @classmethod
    def anime_format(cls, anime_name: str = None):
        directory_path = PathCache.get_directory_path()
        # 未指定动漫名称则取文件夹名称
        if anime_name is None:
            anime_name = directory_path.stem
        # 因为文件名中有动漫名和标题，因此这里排序文件的时候需要特殊处理
        title_pattern = re.compile("「(.*?)」")

        def remove_name_and_title(stem):
            return int(re.sub(r"\D+", "", title_pattern.sub("", stem.replace(anime_name, ""))))

        for index, anime_path in enumerate(cls._sorted_glob(directory_path, remove_name_and_title)):
            # 1) 更改文件名，因为会有文件名已存在的情况，因此这里生成新文件名时需要添加temp防止重复
            title = title_pattern.findall(anime_path.stem)
            anime_stem = f"temp_{anime_name} [{str(index + 1).zfill(2)}] 「{title[0] if title else ''}」"
            # 2) 重命名文件
            cls._rename_path(anime_path, directory_path.joinpath(f"{anime_stem}{anime_path.suffix}"))
        for anime_path in directory_path.glob("*.*"):
            cls._rename_path(anime_path)

    @classmethod
    def manga_format(cls, suffix: str = None, start_number: int = None):
        """格式化漫画"""
        directory_path = PathCache.get_directory_path()
        for manga_path in sorted(cls._sorted_glob(directory_path)):
            # 1) 更改文件名，因为会有文件名已存在的情况，因此这里生成新文件名时需要添加temp防止重复
            manga_stem = manga_path.stem if start_number is None else f"temp_{str(start_number).zfill(3)}"
            start_number += 1
            # 2) 更改文件后缀
            if suffix:
                manga_suffix = suffix if suffix.startswith(".") else f".{suffix}"
            else:
                # 2.2) webp格式强转为jpg后缀
                if re.search(r"\.webp$", manga_path.suffix):
                    manga_suffix = ".jpg"
                else:
                    manga_suffix = manga_path.suffix
            # 3) 重命名文件
            cls._rename_path(manga_path, directory_path.joinpath(f"{manga_stem}{manga_suffix}"))
        for manga_path in directory_path.glob("*.*"):
            cls._rename_path(manga_path)

    @staticmethod
    def _sorted_glob(path: Path, sorted_format_function=None):
        def get_stem(stem):
            return stem if sorted_format_function is None else sorted_format_function(stem)

        return sorted(path.glob("*.*"), key=lambda x: int(re.sub(r"\D+", "", str(get_stem(x.stem)))))

    @staticmethod
    def _rename_path(path: Path, new_path: Path = None):
        """重命名路径"""
        if new_path is None:
            # 重新生成文件路径，防止其父辈文件夹中名称有temp开头的文件夹被误重命名
            new_path = path.parent.joinpath(re.sub(r"^temp_", "", path.stem) + path.suffix)
        if path != new_path:
            os.rename(path, new_path)
