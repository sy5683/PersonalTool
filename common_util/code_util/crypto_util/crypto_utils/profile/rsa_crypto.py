import base64
import typing

import rsa

from ..base.crypto_base import CryptoBase


class RSACrypto(CryptoBase):
    _private_key = None
    _public_key = None

    @classmethod
    def rsa_decrypt(cls, ciphertext: typing.Union[bytes, str]) -> str:
        """rsa解密"""
        if cls._private_key is None:
            with open(cls.get_key_path("rsa_private_key"), "r") as file:
                cls._private_key = rsa.PrivateKey.load_pkcs1(base64.b64decode(file.read()))
        return cls.to_str(rsa.decrypt(base64.b64decode(cls.to_bytes(ciphertext)), cls._private_key))

    @classmethod
    def rsa_encrypt(cls, plaintext: typing.Union[bytes, str]) -> str:
        """rsa加密"""
        if cls._public_key is None:
            with open(cls.get_key_path("rsa_public_key"), "r") as file:
                cls._public_key = rsa.PublicKey.load_pkcs1(base64.b64decode(file.read()))
        return cls.to_str(base64.b64encode(rsa.encrypt(cls.to_bytes(plaintext), cls._public_key)))
