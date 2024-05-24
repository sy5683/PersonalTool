from common_core.base.tool_base import ToolBase
from feature.backuper.browser_backuper import BrowserBackuper


class ComputerBackuper(ToolBase):

    def main(self, *args, **kwargs):
        # 1) 备份谷歌浏览器书签
        BrowserBackuper.backup_chrome_bookmark()


if __name__ == '__main__':
    computer_backuper = ComputerBackuper()
    computer_backuper.main()
