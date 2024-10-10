import os
import shutil
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import subprocess
import psutil
import keyboard

# 常量定义
DISCLAIMER_TEXT = "免责声明: 本软件仅供参考，使用时请自行承担风险。"
AUTHOR_TEXT = "作者: daad_weibai"
VERSION_TEXT = "版本: 1.0.0"
HOME_KEY_LABEL_TEXT = "按 Home 键可一键结束所有非系统进程"

class SystemOptimizerApp:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        self.master.title("系统优化工具 - 版本 1.0.0")
        self.master.geometry("600x590")
        self.master.minsize(400, 560)

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill='both', expand=True)

        self.optimizer_frame = self.create_frame("系统优化")
        self.repair_frame = self.create_frame("修复系统组件")
        self.startup_frame = self.create_frame("启动项管理")

        self.create_optimizer_content()
        self.create_repair_content()
        self.startup_manager = StartupManager(self.startup_frame)

        keyboard.add_hotkey('home', self.terminate_non_system_processes)

    def create_frame(self, title):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        return frame

    def create_optimizer_content(self):
        ttk.Label(self.optimizer_frame, text=DISCLAIMER_TEXT, font=("Microsoft YaHei", 10), foreground="#FF0000").pack(pady=10)
        ttk.Label(self.optimizer_frame, text=AUTHOR_TEXT, font=("Microsoft YaHei", 14)).pack(pady=10)
        ttk.Label(self.optimizer_frame, text=VERSION_TEXT, font=("Microsoft YaHei", 14)).pack(pady=5)
        self.time_label = ttk.Label(self.optimizer_frame, font=("Microsoft YaHei", 24))
        self.time_label.pack(pady=20)
        self.create_buttons()
        self.update_time()

    def create_repair_content(self):
        buttons = [
            ("修复注册表", self.repair_registry),
            ("运行 CMD 命令", self.run_cmd),
            ("修改文件后缀名", self.change_file_extension),
            ("修复任务管理器", self.repair_task_manager),
            ("移除账户锁", self.unlock_account),
            ("一键解毒", self.quick_scan),
            ("一键超级解毒", self.super_scan)
        ]
        for text, command in buttons:
            ttk.Button(self.repair_frame, text=text, command=command, width=20).pack(pady=10, padx=20, fill='x')
        ttk.Label(self.repair_frame, text=HOME_KEY_LABEL_TEXT, font=("Microsoft YaHei", 12), foreground="#0000FF").pack(pady=10)

    # 其他方法保持不变...

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemOptimizerApp(root)
    root.mainloop()
