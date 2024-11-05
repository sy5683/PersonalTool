import hashlib

from .crypto_config import CryptoConfig


class Md5Crypto:

    @staticmethod
    def md5_encrypt(plaintext: str) -> str:
        """md5加密"""
        md5 = hashlib.md5()
        md5.update(plaintext.encode(CryptoConfig.encoding_type))
        return md5.hexdigest()
