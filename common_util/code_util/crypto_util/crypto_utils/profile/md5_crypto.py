import hashlib

from ..base.crypto_base import CryptoBase


class Md5Crypto(CryptoBase):

    @classmethod
    def md5_encrypt(cls, plaintext: str) -> str:
        """md5加密"""
        md5 = hashlib.md5()
        md5.update(plaintext.encode(cls.encoding_type))
        return md5.hexdigest()
