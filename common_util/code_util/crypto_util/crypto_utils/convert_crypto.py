import typing

from .crypto_config import CryptoConfig


class ConvertCrypto:

    @staticmethod
    def to_bytes(value: typing.Union[bytes, str]) -> bytes:
        return value.encode(CryptoConfig.encode_type) if isinstance(value, str) else value

    @staticmethod
    def to_str(value: typing.Union[bytes, str]) -> str:
        return value.decode(CryptoConfig.encode_type) if isinstance(value, bytes) else value
