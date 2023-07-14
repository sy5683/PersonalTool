import re

from .feature.file_feature import FileFeature


class MangaFormat:

    @classmethod
    def manga_format(cls, suffix: str = None, start_number: int = None):
        directory_path = FileFeature.get_directory_path()
        for manga_path in FileFeature.sorted_glob(directory_path):
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
            FileFeature.file_rename(manga_path, directory_path.joinpath(f"{manga_stem}{manga_suffix}"))
        # 收尾操作再次重命名文件，将temp去掉
        for manga_path in directory_path.glob("*.*"):
            FileFeature.file_rename(manga_path)
