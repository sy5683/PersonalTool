import base64
import typing

import rsa
from pathlib import Path

from .convert_crypto import ConvertCrypto


class RSACrypto:
    _private_key = None
    _public_key = None

    @classmethod
    def rsa_decrypt(cls, ciphertext: bytes) -> str:
        """rsa解密"""
        if cls._private_key is None:
            cls._load_keys()
        return ConvertCrypto.to_str(rsa.decrypt(base64.b64decode(ciphertext), cls._private_key))

    @classmethod
    def rsa_encrypt(cls, plaintext: bytes) -> str:
        """rsa加密"""
        if cls._public_key is None:
            cls._load_keys()
        return ConvertCrypto.to_str(base64.b64encode(rsa.encrypt(plaintext, cls._public_key)))

    @classmethod
    def _load_keys(cls):
        def _get_keys_path(file_name: str = ''):
            return Path(__file__).parent.joinpath(f"keys\\{file_name}")

        with open(_get_keys_path("rsa_private_key"), "r") as file:
            cls._private_key = rsa.PrivateKey.load_pkcs1(base64.b64decode(file.read()))
        with open(_get_keys_path("rsa_public_key"), "r") as file:
            cls._public_key = rsa.PublicKey.load_pkcs1(base64.b64decode(file.read()))
