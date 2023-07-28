import re
from pathlib import Path

from .feature.file_feature import FileFeature


class AnimeFormat:

    @classmethod
    def anime_format(cls, anime_name: str = None):
        directory_path = Path(FileFeature.get_directory_path())

        # 未指定动漫名称则取文件夹名称
        if anime_name is None:
            anime_name = directory_path.stem
        # 因为文件名中有动漫名和标题，因此这里排序文件的时候需要特殊处理
        title_pattern = re.compile("「(.*?)」")

        def remove_name_and_title(stem):
            return int(re.sub(r"\D+", "", title_pattern.sub("", stem.replace(anime_name, ""))))

        for index, anime_path in enumerate(FileFeature.sorted_glob(directory_path, remove_name_and_title)):
            # 1) 更改文件名，因为会有文件名已存在的情况，因此这里生成新文件名时需要添加temp防止重复
            title = title_pattern.findall(anime_path.stem)
            anime_stem = f"temp_{anime_name} [{str(index + 1).zfill(2)}] 「{title[0] if title else ''}」"
            # 2) 重命名文件
            FileFeature.file_rename(anime_path, directory_path.joinpath(f"{anime_stem}{anime_path.suffix}"))
        # 收尾操作再次重命名文件，将temp去掉
        for anime_path in directory_path.glob("*.*"):
            FileFeature.file_rename(anime_path)
