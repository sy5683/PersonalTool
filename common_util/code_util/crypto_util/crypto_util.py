import typing

from .crypto_utils.profile.md5_crypto import Md5Crypto
from .crypto_utils.profile.rsa_crypto import RSACrypto


class CryptoUtil:

    @staticmethod
    def md5_encrypt(plaintext: str) -> str:
        """md5加密"""
        return Md5Crypto.md5_encrypt(plaintext)

    @staticmethod
    def rsa_decrypt(ciphertext: typing.Union[bytes, str]) -> str:
        """rsa解密"""
        return RSACrypto.rsa_decrypt(ciphertext)

    @staticmethod
    def rsa_encrypt(plaintext: typing.Union[bytes, str]) -> str:
        """rsa加密"""
        return RSACrypto.rsa_encrypt(plaintext)
