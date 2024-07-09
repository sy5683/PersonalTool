import typing


class ConvertCrypto:

    @staticmethod
    def to_bytes(value: typing.Union[bytes, str]) -> bytes:
        return value.encode("utf-8") if isinstance(value, str) else value

    @staticmethod
    def to_str(value: typing.Union[bytes, str]) -> str:
        return value.decode("utf-8") if isinstance(value, bytes) else value
