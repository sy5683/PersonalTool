import ftplib
import logging
import os

from .base.connect_base import ConnectBase


class FtpConnect(ConnectBase):

    def __init__(self, host: str, port: int, username: str, password: str):
        super().__init__(host, port, username, password)
        self.ftp = None

    def close(self):
        """关闭连接"""
        if self.ftp is not None:
            self.ftp.close()
            self.ftp = None

    def exists(self, remote_path: str) -> bool:
        """判断路径是否存在"""
        ftp = self._get_ftp()
        # noinspection PyBroadException
        try:
            ftp.voidcmd(f"MDTM {remote_path}")[4:].strip()  # 根据是否可以获取修改时间判断路径是否存在
            return True
        except Exception:
            logging.warning(f"ftp服务器中路径不存在: {remote_path}")
            return False

    def upload(self, local_path: str, remote_path: str):
        """上传文件"""
        ftp = self._get_ftp()
        logging.info(f"将本地文件【{os.path.basename(local_path)}】上传到服务器: {remote_path}")
        with open(local_path, 'rb') as fp:
            buff_size = 1024 * 1024 * 1024
            ftp.storbinary('STOR ' + remote_path, fp, buff_size)

    def _get_ftp(self) -> ftplib.FTP:
        """获取ftp连接对象"""
        if not self.ftp:
            logging.info(f"连接ftp服务器: {self._host}:{self._port}")
            self.ftp = ftplib.FTP()
            self.ftp.encoding = "UTF-8"  # 如果数据有中文，这里要将设置改为utf-8
            self.ftp.timeout = 120  # 设置超时时间
            self.ftp.connect(self._host, self._port)
            self.ftp.login(user=self._username, passwd=self._password)
        return self.ftp
