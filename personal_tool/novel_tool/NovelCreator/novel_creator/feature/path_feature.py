from pathlib import Path


class PathFeature:

    @staticmethod
    def to_project_path(relative_path: str = '') -> Path:
        """项目路径"""
        return Path(__file__).parent.parent.joinpath(relative_path)

    @classmethod
    def to_novel_path(cls, novel_name: str = None) -> Path:
        """小说路径"""
        novel_path = cls.to_project_path("小说")
        if novel_name is not None:
            novel_path = novel_path.joinpath(novel_name)
            assert novel_path.is_dir(), f"小说不存在: {novel_name}"
        return novel_path
