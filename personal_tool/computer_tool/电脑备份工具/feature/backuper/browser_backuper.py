import os

from .base.backuper_base import BackuperBase


class BrowserBackuper(BackuperBase):

    @classmethod
    def backup_chrome_bookmark(cls):
        """备份谷歌浏览器书签"""
        for bookmark_path in cls._get_chrome_bookmark_paths():
            cls.backup_file(bookmark_path, "Chrome书签")

    @classmethod
    def update_chrome_bookmark(cls):
        """更新谷歌浏览器书签"""
        for bookmark_path in cls._get_chrome_bookmark_paths():
            cls.update_file(bookmark_path, "Chrome书签")

    @staticmethod
    def _get_chrome_bookmark_paths():
        """获取谷歌浏览器书签路径"""
        user_data_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data",
                                      "Default")
        if not os.path.exists(user_data_path):
            raise FileNotFoundError("未找到谷歌浏览器User Data文件路径")
        for bookmark_name in ["Bookmarks", "Bookmarks.bak"]:
            yield os.path.join(user_data_path, bookmark_name)
