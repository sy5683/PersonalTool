from .dialog_utils.win32_dialog import Win32Dialog


class DialogUtil:

    @staticmethod
    def message_box(content: str, title: str = '弹窗', disable_close: bool = False):
        """消息通知"""
        Win32Dialog.message_box(content, title, disable_close)
