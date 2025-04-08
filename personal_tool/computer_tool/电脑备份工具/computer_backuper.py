from enum import Enum

from common_core.base.tool_base import ToolBase
from feature.backuper.browser_backuper import BrowserBackuper


class Operations(Enum):
    backup_chrome_bookmark = BrowserBackuper.backup_chrome_bookmark
    update_chrome_bookmark = BrowserBackuper.update_chrome_bookmark


class ComputerBackuper(ToolBase):

    def main(self, function, **kwargs):
        function(**kwargs)


if __name__ == '__main__':
    computer_backuper = ComputerBackuper()
    computer_backuper.main(Operations.backup_chrome_bookmark)
    # computer_backuper.main(Operations.update_chrome_bookmark)
