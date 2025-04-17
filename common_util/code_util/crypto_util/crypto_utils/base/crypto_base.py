import abc
import pathlib
import typing


class CryptoBase(metaclass=abc.ABCMeta):
    encoding_type = "UTF-8"

    @classmethod
    def to_bytes(cls, value: typing.Union[bytes, str]) -> bytes:
        return value.encode(cls.encoding_type) if isinstance(value, str) else value

    @classmethod
    def to_str(cls, value: typing.Union[bytes, str]) -> str:
        return value.decode(cls.encoding_type) if isinstance(value, bytes) else value

    @staticmethod
    def get_key_path(file_name: str) -> pathlib.Path:
        """获取秘钥路径"""
        return pathlib.Path(__file__).parent.parent.joinpath("keys", f"{file_name}")
