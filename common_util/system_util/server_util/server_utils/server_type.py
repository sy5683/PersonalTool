import typing
from enum import Enum

from .entity.base.connect_base import ConnectBase
from .entity.ftp_connect import FtpConnect
from .entity.sftp_connect import SftpConnect


class ServerType(Enum):
    ftp = {'connect_class': FtpConnect}
    sftp = {'connect_class': SftpConnect}

    def to_connect_class(self) -> typing.Type[ConnectBase]:
        return self.value['connect_class']
