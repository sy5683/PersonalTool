from common_core.base.test_base import TestBase
from common_util.code_util.crypto_util.crypto_util import CryptoUtil


class CryptoUtilTestCase(TestBase):

    def setUp(self):
        self.plaintext = "测试"

    def test_md5_encrypt(self):
        ciphertext = CryptoUtil.md5_encrypt(self.plaintext)
        print(ciphertext)

    def test_rsa_decrypt(self):
        plaintext = CryptoUtil.rsa_decrypt("lnbLzXrtmxAduDd8ExjGzuU++oRSOH1JfNeGgxQioBY=")
        print(plaintext)

    def test_rsa_encrypt(self):
        ciphertext = CryptoUtil.rsa_encrypt(self.plaintext)
        print(ciphertext)
