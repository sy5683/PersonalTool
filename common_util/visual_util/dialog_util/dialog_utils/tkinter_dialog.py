import tkinter
from tkinter import messagebox


class TkinterDialog:

    @staticmethod
    def message_box(message: str, title: str):
        """消息通知"""
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        messagebox.showinfo(title, message)  # 显示弹窗
