import ftplib

from .base.server_connect import ServerConnect


class FtpConnect(ServerConnect):

    def __init__(self, ip: str, port: int, username: str, password: str, **kwargs):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        super().__init__(f"【FTP】{self.ip}:{self.port}", **kwargs)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        super().__exit__(exc_type, exc_value, exc_traceback)
        if exc_value:
            raise exc_type(exc_value)

    def check_remote_path_exists(self, remote_path: str) -> bool:
        """判断服务器路径是否存在"""
        # noinspection PyBroadException
        try:
            # 根据是否可以获取修改时间判断路径是否存在
            _ = self.connect.voidcmd(f"MDTM {remote_path}")[4:].strip()
            return True
        except Exception:
            return False

    def upload_file(self, local_path: str, remote_path: str):
        """ftp上传文件"""
        with open(local_path, 'rb') as file:
            self.connect.storbinary(f"STOR {remote_path}", file, blocksize=1024 * 1024 * 1024)

    def _get_connect(self):
        """获取连接"""
        self.connect = ftplib.FTP()
        self.connect.encoding = "UTF-8"
        self.connect.timeout = self._timeout
        self.connect.connect(self.ip, self.port)
        self.connect.login(user=self.username, passwd=self.password)
