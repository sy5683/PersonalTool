import hashlib

from .crypto_config import CryptoConfig


class Md5Crypto:

    @staticmethod
    def md5_encrypt(plaintext: str) -> str:
        """md5加密"""
        md5 = hashlib.md5()
        md5.update(plaintext.encode(CryptoConfig.encode_type))
        return md5.hexdigest()
