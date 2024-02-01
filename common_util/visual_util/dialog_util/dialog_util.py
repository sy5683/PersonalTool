from .dialog_utils.win32_dialog import Win32Dialog


class DialogUtil:

    @staticmethod
    def messagebox(content: str, title: str = '弹窗', disable_close: bool = False):
        """消息通知"""
        Win32Dialog.messagebox(content, title, disable_close)
