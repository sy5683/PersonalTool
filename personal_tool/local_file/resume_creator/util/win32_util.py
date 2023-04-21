import win32api


class Win32Util:

    @staticmethod
    def open_file(file_path: str):
        """打开文件"""
        win32api.ShellExecute(0, "open", file_path, "", "", 1)
