from pathlib import Path


class CryptoConfig:
    encoding_type = "UTF-8"

    @staticmethod
    def get_key_path(file_name: str) -> Path:
        """获取秘钥路径"""
        return Path(__file__).parent.joinpath(f"keys\\{file_name}")