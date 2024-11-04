import base64

import rsa

from .convert_crypto import ConvertCrypto
from .crypto_config import CryptoConfig


class RSACrypto:
    _private_key = None
    _public_key = None

    @classmethod
    def rsa_decrypt(cls, ciphertext: bytes) -> str:
        """rsa解密"""
        if cls._private_key is None:
            with open(CryptoConfig.get_key_path("rsa_private_key"), "r") as file:
                cls._private_key = rsa.PrivateKey.load_pkcs1(base64.b64decode(file.read()))
        return ConvertCrypto.to_str(rsa.decrypt(base64.b64decode(ciphertext), cls._private_key))

    @classmethod
    def rsa_encrypt(cls, plaintext: bytes) -> str:
        """rsa加密"""
        if cls._public_key is None:
            with open(CryptoConfig.get_key_path("rsa_public_key"), "r") as file:
                cls._public_key = rsa.PublicKey.load_pkcs1(base64.b64decode(file.read()))
        return ConvertCrypto.to_str(base64.b64encode(rsa.encrypt(plaintext, cls._public_key)))
