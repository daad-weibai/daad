import os
from tkinter import ttk, messagebox
import tkinter as tk

import pystray
from PIL import Image


class SystemOptimizerApp:
    """主系统优化工具应用类，集成所有功能模块。"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("系统优化工具 - 版本 2.0.0")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)  # 调整最小窗口大小以适应内容

        # 初始化系统托盘
        self.icon = None
        # self.create_tray_icon()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        frame = tk.Frame(self.root, borderwidth=2, relief="groove",height=40)
        frame.pack(fill='both')

        # 处理窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    # def create_tray_icon(self):
    #     """创建系统托盘图标和菜单。"""
    #     image_path = self.get_icon_path()
    #     tray_image = Image.open(image_path)
    #
    #     # 定义托盘菜单
    #     menu = (pystray.MenuItem('显示', self.show_window),
    #             pystray.MenuItem('退出', self.exit_app))
    #
    #     self.icon = pystray.Icon("SystemOptimizerApp", tray_image, "系统优化工具", menu)
    #     # self.icon.run()
    #
    # def get_icon_path(self):
    #     """获取托盘图标的路径。如果图标不存在，则创建一个简单的图标。"""
    #     icon_filename = "../daad.ico"
    #     if not os.path.exists(icon_filename):
    #         # 创建一个简单的图标
    #         img = Image.new('RGB', (64, 64), color='blue')
    #         img.save(icon_filename, format='ICO')
    #     return icon_filename

    def hide_window(self):
        """隐藏主窗口并最小化到系统托盘。"""
        self.root.withdraw()

    def show_window(self):
        """显示主窗口并从系统托盘恢复。"""
        self.root.deiconify()

    def exit_app(self):
        """退出应用程序。"""
        # self.icon.run()
        self.root.destroy()

    def on_close(self):
        """处理窗口关闭事件，询问是否隐藏到系统托盘。"""
        if messagebox.askyesno("隐藏到系统托盘", "是否将程序隐藏到系统托盘？"):
            self.hide_window()
        else:
            self.exit_app()


if __name__ == '__main__':
    SystemOptimizerApp()
