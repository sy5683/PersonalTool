import logging
import pathlib
import shutil


class Compress:

    @staticmethod
    def compress(file_path: pathlib.Path, compress_name: str) -> str:
        """压缩文件"""
        compress_path = file_path.parent.joinpath(compress_name if compress_name else file_path.stem)
        try:
            logging.info(f"压缩文件: {file_path} -> {compress_path}")
            return shutil.make_archive(str(compress_path), "zip", root_dir=file_path.parent, base_dir=file_path.name)
        except Exception:
            raise RuntimeError(f"压缩失败: {file_path}")
