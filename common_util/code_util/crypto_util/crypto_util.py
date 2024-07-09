import typing

from .crypto_utils.convert_crypto import ConvertCrypto
from .crypto_utils.md5_crypto import Md5Crypto
from .crypto_utils.rsa_crypto import RSACrypto


class CryptoUtil:

    @staticmethod
    def md5_encrypt(plaintext: str) -> str:
        """md5加密"""
        return Md5Crypto.md5_encrypt(plaintext)

    @staticmethod
    def rsa_decrypt(ciphertext: typing.Union[bytes, str]) -> str:
        """rsa解密"""
        return RSACrypto.rsa_decrypt(ConvertCrypto.to_bytes(ciphertext))

    @staticmethod
    def rsa_encrypt(plaintext: typing.Union[bytes, str]) -> str:
        """rsa加密"""
        return RSACrypto.rsa_encrypt(ConvertCrypto.to_bytes(plaintext))
