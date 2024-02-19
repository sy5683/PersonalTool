from common_core.base.test_base import TestBase
from common_util.system_util.server_util.server_util import ServerUtil


class ServerUtilTestCase(TestBase):

    def test_get_ftp_connect(self):
        server_connect = ServerUtil.get_server_connect()

    def test_get_sftp_connect(self):
        server_connect = ServerUtil.get_server_connect()
