import hashlib


class CryptoUtil:

    @staticmethod
    def to_md5(message: str) -> str:
        """md5加密"""
        md5 = hashlib.md5()
        md5.update(message.encode('utf8'))
        return md5.hexdigest()
