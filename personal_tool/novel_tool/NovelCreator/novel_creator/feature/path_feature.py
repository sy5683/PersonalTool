from pathlib import Path


class PathFeature:

    @classmethod
    def to_novel_path(cls, novel_name: str = '') -> Path:
        """小说路径"""
        novel_path = Path(__file__).parent.parent.joinpath(f"小说\\{novel_name}")
        assert novel_path.is_dir(), f"小说不存在: {novel_name}"
        return novel_path
