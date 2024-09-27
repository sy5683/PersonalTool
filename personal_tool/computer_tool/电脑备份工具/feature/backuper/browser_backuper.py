import logging
import os

from ..backup_feature import BackupFeature


class BrowserBackuper:

    @staticmethod
    def backup_chrome_bookmark():
        """备份谷歌浏览器书签"""
        # 查找User Data文件路径
        user_data_path = os.path.join(os.path.expanduser('~'), "AppData\\Local\\Google\\Chrome\\User Data\\Default")
        if not os.path.exists(user_data_path):
            logging.warning("未找到谷歌浏览器User Data文件路径")
            return
        logging.info(f"谷歌浏览器书签路径: {user_data_path}")
        # 保存文件
        for bookmark_name in ["Bookmarks", "Bookmarks.bak"]:
            bookmark_path = os.path.join(user_data_path, bookmark_name)
            BackupFeature.backup_file(bookmark_path, "Chrome书签")
