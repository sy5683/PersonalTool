from common_core.base.test_base import TestBase
from common_util.system_util.server_util.server_util import ServerUtil


class ServerUtilTestCase(TestBase):

    def setUp(self):
        self.ip = "192.168.20.137"
        self.port = 2121
        self.username = "admin"
        self.password = "D1a1d@m@in"

    def test_get_ftp_connect(self):
        server_connect = ServerUtil.get_server_connect(ip=self.ip, port=self.port, username=self.username,
                                                       password=self.password, server_type='FTP')
        with server_connect:
            pass

    def test_get_sftp_connect(self):
        server_connect = ServerUtil.get_server_connect(ip=self.ip, port=self.port, username=self.username,
                                                       password=self.password, server_type='SFTP')

        with server_connect:
            pass
