import hashlib


class Md5Crypto:

    @staticmethod
    def md5_encrypt(plaintext: str) -> str:
        """md5加密"""
        md5 = hashlib.md5()
        md5.update(plaintext.encode('utf8'))
        return md5.hexdigest()
