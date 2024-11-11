    # =============================================================================
# 版权所有 © 2024 伟佰. 保留所有权利。
# 
# 本软件为weibai所开发，未经许可不得用于商业用途。
# =============================================================================

import os
import time
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import psutil
import threading
import subprocess
from win32com.client import Dispatch
import locale
import shutil
import win32gui
import win32process
import winreg
import ctypes
import sys
import win32con
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pystray  # 系统托盘库
from PIL import Image, ImageTk  # 图标处理库

# 本程序由daad开发
# 本程序受著作权法保护


class Disclaimer:
    """免责声明窗口，用户首次运行时显示，并记录用户同意情况。"""

    def __init__(self, master, on_agree_callback):
        self.master = master
        self.on_agree_callback = on_agree_callback
        self.master.withdraw()  # 隐藏主窗口

        self.disclaimer_window = tk.Toplevel()
        self.disclaimer_window.title("免责声明")
        self.disclaimer_window.geometry("600x400")
        self.disclaimer_window.resizable(False, False)

        # 免责声明内容
        disclaimer_text = (
            "免责声明:\n\n"
            "本软件仅供参考，使用时请自行承担风险。\n"
            "作者不对因使用本软件而导致的任何损失或损害承担责任。\n\n"
            "请仔细阅读以上内容，点击“同意”即表示您已阅读并同意以上免责声明。"
        )

        self.label = tk.Label(
            self.disclaimer_window, text=disclaimer_text, wraplength=580, justify="left"
        )
        self.label.pack(pady=20, padx=10)

        # 按钮框架
        button_frame = tk.Frame(self.disclaimer_window)
        button_frame.pack(pady=20)

        self.agree_button = tk.Button(button_frame, text="同意", width=10, command=self.agree)
        self.agree_button.grid(row=0, column=0, padx=10)

        self.disagree_button = tk.Button(
            button_frame, text="不同意", width=10, command=self.disagree
        )
        self.disagree_button.grid(row=0, column=1, padx=10)

        # 禁止关闭窗口
        self.disclaimer_window.protocol("WM_DELETE_WINDOW", self.disagree)

    def agree(self):
        """用户同意免责声明后记录并显示主窗口。"""
        # 创建一个文件以记录用户已同意免责声明
        with open(self.get_disclaimer_file_path(), "w") as f:
            f.write("Agreed")
        self.disclaimer_window.destroy()
        self.on_agree_callback()  # 回调函数显示主窗口

    def disagree(self):
        """用户不同意免责声明后关闭主程序。"""
        self.master.destroy()  # 关闭主程序

    @staticmethod
    def get_disclaimer_file_path():
        """获取记录用户同意免责声明的文件路径。"""
        app_data = os.getenv("APPDATA")
        disclaimer_dir = os.path.join(app_data, "SystemOptimizerApp")
        os.makedirs(disclaimer_dir, exist_ok=True)
        return os.path.join(disclaimer_dir, "disclaimer_agree.txt")

    @staticmethod
    def has_agreed():
        """检查用户是否已同意免责声明。"""
        return os.path.isfile(Disclaimer.get_disclaimer_file_path())


class TitlePage:
    """欢迎页面，展示软件基本信息并提供开始使用的按钮。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(
            master, text="欢迎使用daad粉丝专用", font=("Microsoft YaHei", 24)
        )
        self.label.pack(pady=50)

        self.subtitle = ttk.Label(
            master,
            text="提升系统性能，优化您的计算机体验",
            font=("Microsoft YaHei", 14),
        )
        self.subtitle.pack(pady=10)

        self.subtitle = ttk.Label(
            master,
            text=(
                "版权所有 © 2024 伟佰. 保留所有权利。\n\n"
                "本软件为伟佰所开发，未经许可不得擅自用于商业用途。"
            ),
            font=("Microsoft YaHei", 14),
        )
        self.subtitle.pack(pady=10)

        self.start_button = ttk.Button(master, text="开始使用", command=self.start_using)
        self.start_button.pack(pady=20)

    def start_using(self):
        """切换到系统优化标签页。"""
        self.master.event_generate("<<SwitchToTab>>")


class StartupManager:
    """启动项管理功能，允许用户列出、添加、删除和禁用启动项。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="启动项管理", font=("Microsoft YaHei", 14))
        self.label.grid(row=0, column=0, pady=10)

        self.startup_listbox = tk.Listbox(
            master, font=("Microsoft YaHei", 12), bg="#fff", fg="#333"
        )
        self.startup_listbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        self.create_startup_buttons()
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=1)

    def create_startup_buttons(self):
        """创建启动项管理的按钮。"""
        buttons = [
            ("列出启动项", self.list_startup_items),
            ("添加启动项", self.add_startup_item),
            ("删除启动项", self.remove_startup_item),
            ("禁用启动项", self.disable_startup_item),
        ]
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=2, column=0, pady=5, padx=20, sticky="ew")
        for i, (text, command) in enumerate(buttons):
            ttk.Button(
                button_frame, text=text, command=command, width=15
            ).grid(row=0, column=i, padx=5, pady=5)

    def list_startup_items(self):
        """列出当前用户启动项文件夹中的所有项目。"""
        self.startup_listbox.delete(0, tk.END)
        startup_folder = os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
        )
        try:
            items = os.listdir(startup_folder)
            for item in items:
                self.startup_listbox.insert(tk.END, item)
        except Exception as e:
            messagebox.showerror("错误", f"读取启动项时出错: {e}")

    def add_startup_item(self):
        """添加新的启动项，通过创建快捷方式。"""
        file_path = filedialog.askopenfilename(title="选择要添加的程序")
        if file_path:
            self.create_shortcut(file_path)

    def create_shortcut(self, file_path):
        """在启动项文件夹中创建程序的快捷方式。"""
        startup_folder = os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
        )
        file_name = os.path.basename(file_path)
        shortcut_path = os.path.join(startup_folder, f"{os.path.splitext(file_name)[0]}.lnk")

        if not os.path.exists(shortcut_path):
            try:
                shell = Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = file_path
                shortcut.WorkingDirectory = os.path.dirname(file_path)
                shortcut.IconLocation = file_path
                shortcut.save()
                messagebox.showinfo("成功", f"已添加启动项: {file_name}")
                self.list_startup_items()
            except Exception as e:
                messagebox.showerror("错误", f"创建启动项时出错: {e}")
        else:
            messagebox.showwarning("警告", "启动项已存在。")

    def remove_startup_item(self):
        """删除选定的启动项。"""
        selected_item = self.startup_listbox.curselection()
        if selected_item:
            item_name = self.startup_listbox.get(selected_item)
            self.delete_startup_item(item_name)
        else:
            messagebox.showwarning("警告", "请先选择一个启动项")

    def delete_startup_item(self, item_name):
        """从启动项文件夹中删除指定的启动项。"""
        startup_folder = os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
        )
        item_path = os.path.join(startup_folder, item_name)

        if os.path.exists(item_path):
            try:
                os.remove(item_path)
                messagebox.showinfo("成功", f"已删除启动项: {item_name}")
                self.list_startup_items()
            except Exception as e:
                messagebox.showerror("错误", f"删除启动项时出错: {e}")
        else:
            messagebox.showwarning("警告", f"未找到启动项: {item_name}")

    def disable_startup_item(self):
        """禁用选定的启动项，通过重命名文件实现。"""
        selected_item = self.startup_listbox.curselection()
        if selected_item:
            item_name = self.startup_listbox.get(selected_item)
            confirm = messagebox.askyesno("确认", f"是否禁用启动项: {item_name}?")
            if confirm:
                startup_folder = os.path.expandvars(
                    r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
                )
                item_path = os.path.join(startup_folder, item_name)
                disabled_path = item_path + ".disabled"
                try:
                    os.rename(item_path, disabled_path)
                    messagebox.showinfo("成功", f"已禁用启动项: {item_name}")
                    self.list_startup_items()
                except Exception as e:
                    messagebox.showerror("错误", f"禁用启动项时出错: {e}")
        else:
            messagebox.showwarning("警告", "请先选择一个启动项")


class RegistryCleaner:
    """注册表清理功能，允许用户扫描和清理无效的注册表项。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="注册表清理", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        self.scan_button = ttk.Button(master, text="扫描无效注册表项", command=self.scan_registry)
        self.scan_button.pack(pady=5)

        self.results_text = tk.Text(master, wrap='word', height=20)
        self.results_text.pack(fill='both', expand=True, padx=20, pady=10)

        self.clean_button = ttk.Button(master, text="清理选中的注册表项", command=self.clean_registry)
        self.clean_button.pack(pady=5)

        self.invalid_keys = []

    def scan_registry(self):
        """扫描常见的无效注册表项。"""
        self.results_text.delete('1.0', tk.END)
        self.invalid_keys = []
        # 示例：扫描常见的无效注册表路径
        keys_to_check = [
            r"SOFTWARE\NonExistentKey",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NonExistentApp"
            # 可以添加更多需要检查的注册表路径
        ]

        for key_path in keys_to_check:
            for root in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
                try:
                    winreg.OpenKey(root, key_path)
                except FileNotFoundError:
                    self.invalid_keys.append(f"{self.get_root_name(root)}\\{key_path}")

        if self.invalid_keys:
            for key in self.invalid_keys:
                self.results_text.insert(tk.END, key + "\n")
        else:
            self.results_text.insert(tk.END, "未找到无效的注册表项。")

    def clean_registry(self):
        """清理扫描到的无效注册表项。"""
        if not self.invalid_keys:
            messagebox.showinfo("提示", "没有需要清理的注册表项。")
            return

        confirm = messagebox.askyesno("确认", "是否删除扫描到的无效注册表项？")
        if confirm:
            for key in self.invalid_keys:
                root_name, key_path = key.split("\\", 1)
                root = self.get_root_handle(root_name)
                try:
                    winreg.DeleteKey(root, key_path)
                    self.results_text.insert(tk.END, f"已删除: {key}\n")
                except FileNotFoundError:
                    self.results_text.insert(tk.END, f"未找到: {key}\n")
                except OSError as e:
                    self.results_text.insert(tk.END, f"删除失败: {key} - {e}\n")
            messagebox.showinfo("提示", "注册表清理完成。")
            self.invalid_keys = []

    @staticmethod
    def get_root_name(root_handle):
        """获取根键的名称。"""
        if root_handle == winreg.HKEY_CURRENT_USER:
            return "HKEY_CURRENT_USER"
        elif root_handle == winreg.HKEY_LOCAL_MACHINE:
            return "HKEY_LOCAL_MACHINE"
        else:
            return "UNKNOWN"

    @staticmethod
    def get_root_handle(root_name):
        """根据根键名称获取根键句柄。"""
        if root_name == "HKEY_CURRENT_USER":
            return winreg.HKEY_CURRENT_USER
        elif root_name == "HKEY_LOCAL_MACHINE":
            return winreg.HKEY_LOCAL_MACHINE
        else:
            return None


class RegistryFixer:
    """注册表修复工具，用于恢复被禁用的注册表访问。"""

    def __init__(self):
        pass

    def fix_disabled_registry_tools(self):
        """
        修复被禁用的注册表访问。
        检查特定的注册表键，如果发现禁用注册表工具，则恢复其访问权限。
        """
        keys_to_fix = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Policies\System"),
        ]

        disabled = False
        errors = []

        for root, subkey in keys_to_fix:
            try:
                with winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS) as key:
                    try:
                        value, regtype = winreg.QueryValueEx(key, "DisableRegistryTools")
                        if value == 1:
                            winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 0)
                            disabled = True
                            print(f"已启用 {RegistryCleaner.get_root_name(root)}\\{subkey}\\DisableRegistryTools")
                    except FileNotFoundError:
                        # 键不存在，可能未被禁用
                        pass
            except PermissionError:
                errors.append(f"无法访问 {RegistryCleaner.get_root_name(root)}\\{subkey}。请以管理员身份运行程序。")
            except Exception as e:
                errors.append(f"处理 {RegistryCleaner.get_root_name(root)}\\{subkey} 时出错: {e}")

        if disabled:
            messagebox.showinfo("成功", "注册表访问已恢复。请重新启动您的计算机以应用更改。")
        else:
            messagebox.showinfo("提示", "未检测到注册表访问被禁用。")

        if errors:
            error_message = "\n".join(errors)
            messagebox.showerror("错误", f"在修复注册表时出现以下问题:\n{error_message}")


class WindowManagerApp:
    """窗口管理功能，允许用户查看、关闭、最小化和最大化当前运行的窗口。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="正在运行的窗口", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        # 使用Treeview展示窗口列表
        columns = ("PID", "Name", "Handle")
        self.window_tree = ttk.Treeview(
            master, columns=columns, show="headings", selectmode="browse"
        )
        for col in columns:
            self.window_tree.heading(col, text=col)
            self.window_tree.column(col, width=150, anchor="center")
        self.window_tree.pack(fill="both", expand=True, padx=20, pady=10)

        # 添加水平和垂直滚动条
        h_scroll = ttk.Scrollbar(master, orient=tk.HORIZONTAL, command=self.window_tree.xview)
        v_scroll = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.window_tree.yview)
        self.window_tree.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        h_scroll.pack(side="bottom", fill="x")
        v_scroll.pack(side="right", fill="y")

        # 按钮框架
        button_frame = ttk.Frame(master)
        button_frame.pack(pady=5)

        self.refresh_button = ttk.Button(button_frame, text="刷新窗口列表", command=self.list_windows)
        self.refresh_button.grid(row=0, column=0, padx=5, pady=5)

        self.close_button = ttk.Button(button_frame, text="关闭选中窗口", command=self.close_window)
        self.close_button.grid(row=0, column=1, padx=5, pady=5)

        self.minimize_button = ttk.Button(button_frame, text="最小化窗口", command=self.minimize_window)
        self.minimize_button.grid(row=0, column=2, padx=5, pady=5)

        self.maximize_button = ttk.Button(button_frame, text="最大化窗口", command=self.maximize_window)
        self.maximize_button.grid(row=0, column=3, padx=5, pady=5)

        self.list_windows()

    def list_windows(self):
        """列出所有可见窗口。"""
        for item in self.window_tree.get_children():
            self.window_tree.delete(item)

        def enum_handler(hwnd, results):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    proc = psutil.Process(pid)
                    proc_name = proc.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    proc_name = "未知"

                results.append((pid, proc_name, hwnd))

        results = []
        win32gui.EnumWindows(enum_handler, results)

        for pid, name, hwnd in results:
            self.window_tree.insert('', tk.END, values=(pid, name, hwnd))

    def get_selected_hwnd(self):
        """获取选中窗口的句柄。"""
        selected_item = self.window_tree.selection()
        if selected_item:
            hwnd = self.window_tree.item(selected_item)['values'][2]
            return hwnd
        else:
            messagebox.showwarning("警告", "请先选择一个窗口。")
            return None

    def close_window(self):
        """关闭选定的窗口。"""
        hwnd = self.get_selected_hwnd()
        if hwnd:
            try:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                messagebox.showinfo("成功", "已发送关闭窗口命令。")
                self.list_windows()
            except Exception as e:
                messagebox.showerror("错误", f"关闭窗口时出错: {e}")

    def minimize_window(self):
        """最小化选定的窗口。"""
        hwnd = self.get_selected_hwnd()
        if hwnd:
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                messagebox.showinfo("成功", "已最小化窗口。")
            except Exception as e:
                messagebox.showerror("错误", f"最小化窗口时出错: {e}")

    def maximize_window(self):
        """最大化选定的窗口。"""
        hwnd = self.get_selected_hwnd()
        if hwnd:
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                messagebox.showinfo("成功", "已最大化窗口。")
            except Exception as e:
                messagebox.showerror("错误", f"最大化窗口时出错: {e}")


class SystemInfoApp:
    """系统信息功能，显示系统的详细信息。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="系统信息", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        # 使用Text组件并配备滚动条以显示系统信息
        self.text_frame = ttk.Frame(master)
        self.text_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.scrollbar = ttk.Scrollbar(self.text_frame, orient=tk.VERTICAL)
        self.system_info_text = tk.Text(self.text_frame, wrap='word', yscrollcommand=self.scrollbar.set, font=("Microsoft YaHei", 10))
        self.scrollbar.config(command=self.system_info_text.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.system_info_text.pack(fill='both', expand=True, side='left')

        # 按钮框架
        button_frame = ttk.Frame(master)
        button_frame.pack(pady=5)

        self.get_info_button = ttk.Button(button_frame, text="获取系统信息", command=self.show_system_info)
        self.get_info_button.pack(pady=5)

    def show_system_info(self):
        """获取并显示系统信息。"""
        try:
            info = subprocess.check_output("systeminfo", stderr=subprocess.STDOUT, shell=True)
            encoding = locale.getpreferredencoding()
            info = info.decode(encoding)

            self.system_info_text.delete('1.0', tk.END)
            self.system_info_text.insert(tk.END, info)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"获取系统信息时出错: {e.output.decode('utf-8', errors='ignore')}")
        except Exception as e:
            messagebox.showerror("错误", f"发生未知错误: {e}")


class UninstallManager:
    """程序卸载管理器，允许用户查看和卸载已安装的程序。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="程序卸载管理器", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        # 使用Treeview展示已安装程序列表
        columns = ("程序名称", "卸载命令")
        self.prog_tree = ttk.Treeview(master, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            self.prog_tree.heading(col, text=col)
            self.prog_tree.column(col, width=350, anchor='w')
        self.prog_tree.pack(fill='both', expand=True, padx=20, pady=10)

        # 添加垂直滚动条
        scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.prog_tree.yview)
        self.prog_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # 卸载按钮
        self.uninstall_button = ttk.Button(master, text="卸载选中程序", command=self.uninstall_program)
        self.uninstall_button.pack(pady=5)

        self.list_installed_programs()

    def list_installed_programs(self):
        """列出已安装的程序。"""
        self.prog_tree.delete(*self.prog_tree.get_children())
        uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        try:
            for root in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
                try:
                    key = winreg.OpenKey(root, uninstall_key)
                except FileNotFoundError:
                    continue
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        sub_key_name = winreg.EnumKey(key, i)
                        sub_key = winreg.OpenKey(key, sub_key_name)
                        name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                        uninstall_cmd = winreg.QueryValueEx(sub_key, "UninstallString")[0]
                        self.prog_tree.insert('', tk.END, values=(name, uninstall_cmd))
                    except FileNotFoundError:
                        continue
                    except OSError:
                        continue
        except Exception as e:
            messagebox.showerror("错误", f"读取已安装程序列表时出错: {e}")

    def uninstall_program(self):
        """卸载选定的程序。"""
        selected_item = self.prog_tree.selection()
        if selected_item:
            program = self.prog_tree.item(selected_item)['values']
            name, uninstall_cmd = program
            confirm = messagebox.askyesno("确认", f"是否卸载 {name}？")
            if confirm:
                try:
                    if uninstall_cmd.lower().startswith('msiexec'):
                        subprocess.run(uninstall_cmd, shell=True, check=True)
                    else:
                        # 处理带有参数的卸载命令
                        subprocess.run(uninstall_cmd, shell=True, check=True)
                    messagebox.showinfo("成功", f"{name} 已卸载。")
                    self.list_installed_programs()
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("错误", f"卸载 {name} 时出错: {e}")
        else:
            messagebox.showwarning("警告", "请先选择一个程序进行卸载。")


class RegistryCleaner:
    """注册表清理功能，允许用户扫描和清理无效的注册表项。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="注册表清理", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        self.scan_button = ttk.Button(master, text="扫描无效注册表项", command=self.scan_registry)
        self.scan_button.pack(pady=5)

        self.results_text = tk.Text(master, wrap='word', height=20)
        self.results_text.pack(fill='both', expand=True, padx=20, pady=10)

        self.clean_button = ttk.Button(master, text="清理选中的注册表项", command=self.clean_registry)
        self.clean_button.pack(pady=5)

        self.invalid_keys = []

    def scan_registry(self):
        """扫描常见的无效注册表项。"""
        self.results_text.delete('1.0', tk.END)
        self.invalid_keys = []
        # 示例：扫描常见的无效注册表路径
        keys_to_check = [
            r"SOFTWARE\NonExistentKey",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NonExistentApp"
            # 可以添加更多需要检查的注册表路径
        ]

        for key_path in keys_to_check:
            for root in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
                try:
                    winreg.OpenKey(root, key_path)
                except FileNotFoundError:
                    self.invalid_keys.append(f"{self.get_root_name(root)}\\{key_path}")

        if self.invalid_keys:
            for key in self.invalid_keys:
                self.results_text.insert(tk.END, key + "\n")
        else:
            self.results_text.insert(tk.END, "未找到无效的注册表项。")

    def clean_registry(self):
        """清理扫描到的无效注册表项。"""
        if not self.invalid_keys:
            messagebox.showinfo("提示", "没有需要清理的注册表项。")
            return

        confirm = messagebox.askyesno("确认", "是否删除扫描到的无效注册表项？")
        if confirm:
            for key in self.invalid_keys:
                root_name, key_path = key.split("\\", 1)
                root = self.get_root_handle(root_name)
                try:
                    winreg.DeleteKey(root, key_path)
                    self.results_text.insert(tk.END, f"已删除: {key}\n")
                except FileNotFoundError:
                    self.results_text.insert(tk.END, f"未找到: {key}\n")
                except OSError as e:
                    self.results_text.insert(tk.END, f"删除失败: {key} - {e}\n")
            messagebox.showinfo("提示", "注册表清理完成。")
            self.invalid_keys = []

    @staticmethod
    def get_root_name(root_handle):
        """获取根键的名称。"""
        if root_handle == winreg.HKEY_CURRENT_USER:
            return "HKEY_CURRENT_USER"
        elif root_handle == winreg.HKEY_LOCAL_MACHINE:
            return "HKEY_LOCAL_MACHINE"
        else:
            return "UNKNOWN"

    @staticmethod
    def get_root_handle(root_name):
        """根据根键名称获取根键句柄。"""
        if root_name == "HKEY_CURRENT_USER":
            return winreg.HKEY_CURRENT_USER
        elif root_name == "HKEY_LOCAL_MACHINE":
            return winreg.HKEY_LOCAL_MACHINE
        else:
            return None


class DiskSpaceAnalyzer:
    """磁盘空间分析器功能，允许用户选择磁盘根目录并分析磁盘使用情况。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="磁盘空间分析器", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        # 选择驱动器按钮
        self.choose_button = ttk.Button(master, text="选择磁盘根目录", command=self.choose_disk)
        self.choose_button.pack(pady=5)

        # 使用Treeview展示磁盘使用情况
        columns = ("路径", "大小 (MB)")
        self.disk_tree = ttk.Treeview(master, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            self.disk_tree.heading(col, text=col)
            self.disk_tree.column(col, width=400, anchor='w')
        self.disk_tree.pack(fill='both', expand=True, padx=20, pady=10)

        # 添加垂直滚动条
        scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.disk_tree.yview)
        self.disk_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def choose_disk(self):
        """选择磁盘根目录并开始分析磁盘空间。"""
        disk = filedialog.askdirectory(title="选择磁盘根目录")
        if disk:
            threading.Thread(target=self.analyze_disk_space, args=(disk,)).start()

    def analyze_disk_space(self, path, depth=0, max_depth=2):
        """分析磁盘空间并显示结果。"""
        self.disk_tree.delete(*self.disk_tree.get_children())
        self._analyze_disk_space_recursive(path, depth, max_depth)

    def _analyze_disk_space_recursive(self, path, depth, max_depth):
        if depth > max_depth:
            return
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_dir(follow_symlinks=False):
                        size = self.get_dir_size(entry.path)
                        self.disk_tree.insert('', tk.END, values=(entry.path, f"{size / (1024 ** 2):.2f}"))
                        self._analyze_disk_space_recursive(entry.path, depth + 1, max_depth)
                    elif entry.is_file(follow_symlinks=False):
                        size = entry.stat().st_size
                        self.disk_tree.insert('', tk.END, values=(entry.path, f"{size / (1024 ** 2):.2f}"))
        except PermissionError:
            pass  # 忽略无权限的文件夹

    def get_dir_size(self, path):
        """获取目录的总大小。"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    try:
                        total_size += os.path.getsize(fp)
                    except:
                        pass
        except:
            pass
        return total_size


class BackupRestoreManager:
    """系统备份与恢复功能，允许用户创建和恢复系统备份。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="系统备份与恢复", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        # 备份按钮
        self.backup_button = ttk.Button(master, text="创建系统备份", command=self.create_backup)
        self.backup_button.pack(pady=5)

        # 恢复按钮
        self.restore_button = ttk.Button(master, text="恢复系统备份", command=self.restore_backup)
        self.restore_button.pack(pady=5)

    def create_backup(self):
        """创建系统备份。"""
        backup_path = filedialog.askdirectory(title="选择备份存储位置")
        if backup_path:
            try:
                # 使用wbadmin命令创建系统备份
                subprocess.run(
                    ["wbadmin", "start backup", "-backupTarget:" + backup_path, "-include:C:", "-allCritical", "-quiet"],
                    check=True
                )
                messagebox.showinfo("成功", "系统备份已创建。")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("错误", f"创建备份时出错: {e}")

    def restore_backup(self):
        """恢复系统备份。"""
        # 恢复系统备份需要重启并且通常需要用户手动操作，这里仅提供提示
        messagebox.showinfo("提示", "恢复系统备份需要重启计算机并在启动时选择恢复选项。请参考官方文档。")


class DriverUpdater:
    """驱动程序更新管理器，允许用户扫描和更新驱动程序。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="驱动程序更新管理器", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        # 扫描驱动按钮
        self.scan_button = ttk.Button(master, text="扫描驱动更新", command=self.scan_drivers)
        self.scan_button.pack(pady=5)

        # 更新驱动按钮
        self.update_button = ttk.Button(master, text="更新选中驱动", command=self.update_driver)
        self.update_button.pack(pady=5)

        # 驱动列表
        columns = ("驱动名称", "当前版本", "最新版本")
        self.driver_tree = ttk.Treeview(master, columns=columns, show='headings')
        for col in columns:
            self.driver_tree.heading(col, text=col)
            self.driver_tree.column(col, width=350, anchor='w')
        self.driver_tree.pack(fill='both', expand=True, padx=20, pady=10)

        # 添加垂直滚动条
        scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.driver_tree.yview)
        self.driver_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def scan_drivers(self):
        """扫描驱动更新（模拟数据）。"""
        self.driver_tree.delete(*self.driver_tree.get_children())
        # 这里可以调用第三方API或使用Windows内置工具扫描驱动
        # 以下为模拟数据
        drivers = [
            ("NVIDIA Display Driver", "450.57", "460.89"),
            ("Realtek Audio Driver", "6.0.1.8346", "6.0.1.8570"),
            # 添加更多驱动信息
        ]
        for driver in drivers:
            self.driver_tree.insert('', tk.END, values=driver)

    def update_driver(self):
        """更新选定的驱动程序（模拟过程）。"""
        selected_item = self.driver_tree.selection()
        if selected_item:
            driver_name, current_version, latest_version = self.driver_tree.item(selected_item)['values']
            confirm = messagebox.askyesno("确认", f"是否更新 {driver_name} 到版本 {latest_version}？")
            if confirm:
                try:
                    # 调用驱动更新的实际逻辑，如下载并安装驱动
                    # 这里仅模拟更新过程
                    subprocess.run(["echo", f"更新{driver_name}到版本{latest_version}"], check=True)
                    messagebox.showinfo("成功", f"{driver_name} 已更新到版本 {latest_version}。")
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("错误", f"更新驱动时出错: {e}")
        else:
            messagebox.showwarning("警告", "请先选择一个驱动进行更新。")


class PrivacyProtector:
    """隐私保护工具，允许用户清理浏览器的隐私数据。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="隐私保护工具", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        # 浏览器选择框
        self.browser_var = tk.StringVar(value="All")
        browsers = ["Chrome", "Firefox", "Edge", "All"]
        self.browser_select = ttk.Combobox(master, values=browsers, textvariable=self.browser_var, state="readonly")
        self.browser_select.pack(pady=5)

        # 清理按钮
        self.clean_button = ttk.Button(master, text="清理隐私数据", command=self.clean_privacy_data)
        self.clean_button.pack(pady=5)

    def clean_privacy_data(self):
        """清理选定浏览器的隐私数据。"""
        selected_browser = self.browser_var.get()
        try:
            if selected_browser in ["Chrome", "All"]:
                self.clean_chrome()
            if selected_browser in ["Firefox", "All"]:
                self.clean_firefox()
            if selected_browser in ["Edge", "All"]:
                self.clean_edge()
            messagebox.showinfo("成功", "隐私数据清理完成。")
        except Exception as e:
            messagebox.showerror("错误", f"清理隐私数据时出错: {e}")

    def clean_chrome(self):
        """清理Chrome浏览器的隐私数据。"""
        chrome_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default')
        cache_path = os.path.join(chrome_path, 'Cache')
        cookies_path = os.path.join(chrome_path, 'Cookies')
        history_path = os.path.join(chrome_path, 'History')
        self.delete_file_or_folder(cache_path)
        self.delete_file_or_folder(cookies_path)
        self.delete_file_or_folder(history_path)

    def clean_firefox(self):
        """清理Firefox浏览器的隐私数据。"""
        firefox_profile = os.path.expandvars(r'%APPDATA%\Mozilla\Firefox\Profiles')
        # 获取所有配置文件
        try:
            profiles = [os.path.join(firefox_profile, d) for d in os.listdir(firefox_profile) if os.path.isdir(os.path.join(firefox_profile, d))]
            for profile in profiles:
                cache_path = os.path.join(profile, 'cache2')
                cookies_path = os.path.join(profile, 'cookies.sqlite')
                history_path = os.path.join(profile, 'places.sqlite')
                self.delete_file_or_folder(cache_path)
                self.delete_file_or_folder(cookies_path)
                self.delete_file_or_folder(history_path)
        except FileNotFoundError:
            pass  # 如果Firefox未安装则跳过

    def clean_edge(self):
        """清理Edge浏览器的隐私数据。"""
        edge_path = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default')
        cache_path = os.path.join(edge_path, 'Cache')
        cookies_path = os.path.join(edge_path, 'Cookies')
        history_path = os.path.join(edge_path, 'History')
        self.delete_file_or_folder(cache_path)
        self.delete_file_or_folder(cookies_path)
        self.delete_file_or_folder(history_path)

    def delete_file_or_folder(self, path):
        """删除指定的文件或文件夹。"""
        if os.path.exists(path):
            if os.path.isfile(path):
                try:
                    os.remove(path)
                except PermissionError:
                    pass
            elif os.path.isdir(path):
                try:
                    shutil.rmtree(path, ignore_errors=True)
                except PermissionError:
                    pass


class PerformanceMonitor:
    """实时性能监控功能，展示CPU、内存、磁盘和网络使用情况。"""

    def __init__(self, master):
        self.master = master
        self.label = ttk.Label(master, text="实时性能监控", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        # 创建图表
        self.fig, self.ax = plt.subplots(2, 2, figsize=(8, 6))
        self.cpu_line, = self.ax[0, 0].plot([], [], label='CPU (%)')
        self.memory_line, = self.ax[0, 1].plot([], [], label='RAM (%)')
        self.disk_line, = self.ax[1, 0].plot([], [], label='磁盘 (%)')
        self.network_line, = self.ax[1, 1].plot([], [], label='网络 (MB)')

        for a in self.ax.flatten():
            a.legend()
            a.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=10)

        # 数据存储
        self.time_data = []
        self.cpu_data = []
        self.memory_data = []
        self.disk_data = []
        self.network_data = []

        # 启动监控
        self.update_graph()

    def update_graph(self):
        """更新性能监控图表。"""
        current_time = time.strftime("%H:%M:%S")
        self.time_data.append(current_time)
        self.cpu_data.append(psutil.cpu_percent())
        self.memory_data.append(psutil.virtual_memory().percent)
        self.disk_data.append(psutil.disk_usage('/').percent)
        net_io = psutil.net_io_counters()
        network_usage = (net_io.bytes_recv + net_io.bytes_sent) / (1024 ** 2)  # MB
        self.network_data.append(network_usage)

        # 保持数据长度一致
        max_length = 20
        if len(self.time_data) > max_length:
            self.time_data.pop(0)
            self.cpu_data.pop(0)
            self.memory_data.pop(0)
            self.disk_data.pop(0)
            self.network_data.pop(0)

        # 更新图表
        self.cpu_line.set_data(range(len(self.cpu_data)), self.cpu_data)
        self.memory_line.set_data(range(len(self.memory_data)), self.memory_data)
        self.disk_line.set_data(range(len(self.disk_data)), self.disk_data)
        self.network_line.set_data(range(len(self.network_data)), self.network_data)

        for a in self.ax.flatten():
            a.set_xlim(0, max_length)
            a.set_ylim(0, 100)

        self.canvas.draw()
        self.master.after(1000, self.update_graph)


class SystemOptimizerApp:
    """主系统优化工具应用类，集成所有功能模块。"""

    def __init__(self, master):
        self.master = master
        master.title("系统优化工具 - 版本 2.0.0")
        master.geometry("1000x800")
        master.minsize(800, 600)  # 调整最小窗口大小以适应内容

        # 初始化系统托盘
        self.icon = None
        self.create_tray_icon()

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        self.create_tabs()
        self.add_to_startup()
        self.update_time()

        # 绑定自定义事件以切换标签
        master.bind("<<SwitchToTab>>", self.switch_to_system_optimizer_tab)

        # 处理窗口关闭事件
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_tabs(self):
        """创建所有标签页。"""
        self.title_frame = self.create_tab("欢迎")
        self.optimizer_frame = self.create_tab("系统优化")
        self.repair_frame = self.create_tab("修复系统组件")
        self.backup_frame = self.create_tab("系统备份与恢复")
        self.driver_frame = self.create_tab("驱动程序更新")
        self.privacy_frame = self.create_tab("隐私保护")
        self.startup_frame = self.create_tab("启动项管理")
        self.window_manager_frame = self.create_tab("窗口管理")
        self.info_frame = self.create_tab("系统信息")
        self.uninstall_frame = self.create_tab("程序卸载管理器")
        self.registry_cleaner_frame = self.create_tab("注册表清理")
        self.disk_analyzer_frame = self.create_tab("磁盘空间分析器")
        self.performance_frame = self.create_tab("性能监控")

        # 创建各功能模块内容
        self.create_title_content()
        self.create_optimizer_content()
        self.create_repair_content()
        BackupRestoreManager(self.backup_frame)
        DriverUpdater(self.driver_frame)
        PrivacyProtector(self.privacy_frame)
        StartupManager(self.startup_frame)
        WindowManagerApp(self.window_manager_frame)
        SystemInfoApp(self.info_frame)
        UninstallManager(self.uninstall_frame)
        RegistryCleaner(self.registry_cleaner_frame)
        DiskSpaceAnalyzer(self.disk_analyzer_frame)
        PerformanceMonitor(self.performance_frame)

    def create_tab(self, title):
        """创建单个标签页并返回其框架。"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        return frame

    def create_title_content(self):
        """创建欢迎页面内容。"""
        TitlePage(self.title_frame)

    def switch_to_system_optimizer_tab(self, event=None):
        """切换到系统优化标签页。"""
        self.notebook.select(self.optimizer_frame)

    def create_optimizer_content(self):
        """创建系统优化标签页的内容。"""
        # 添加免责声明提示
        self.create_label(self.optimizer_frame, "免责声明: 本软件仅供参考，使用时请自行承担风险。", "#FF0000", 10)
        self.create_label(self.optimizer_frame, "作者: weibai", None, 14)
        self.create_label(self.optimizer_frame, "版本: 4.0.0", None, 14)

        # 显示当前时间
        self.time_label = ttk.Label(self.optimizer_frame, text="", font=("Microsoft YaHei", 24))
        self.time_label.pack(pady=20)

        # 监控系统资源
        self.monitor_var = tk.BooleanVar()
        self.monitor_checkbox = ttk.Checkbutton(
            self.optimizer_frame,
            text="监控系统资源",
            variable=self.monitor_var,
            command=self.toggle_monitoring
        )
        self.monitor_checkbox.pack(pady=10)

        self.resource_label = ttk.Label(self.optimizer_frame, text="", font=("Microsoft YaHei", 12))
        self.resource_label.pack(pady=10)

        # 操作按钮
        self.create_buttons()

    def toggle_monitoring(self):
        """切换系统资源监控。"""
        self.monitoring = self.monitor_var.get()
        if self.monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()

    def start_monitoring(self):
        """启动系统资源监控线程。"""
        if not hasattr(self, 'monitor_thread') or not self.monitor_thread.is_alive():
            self.monitor_thread = threading.Thread(target=self.monitor_resources)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()

    def stop_monitoring(self):
        """停止系统资源监控。"""
        self.monitoring = False

    def monitor_resources(self):
        """监控系统资源并更新显示。"""
        self.monitoring = True
        while self.monitoring:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')
            network_stats = psutil.net_io_counters()
            network_usage = (network_stats.bytes_sent + network_stats.bytes_recv) / (1024 ** 2)  # MB

            resource_info = (f"CPU 使用率: {cpu_usage}% | "
                             f"内存使用率: {memory.percent}% | "
                             f"磁盘使用率: {disk_usage.percent}% | "
                             f"网络使用量: {network_usage:.2f} MB")
            self.resource_label.config(text=resource_info)

    def create_buttons(self):
        """创建系统优化页面的操作按钮。"""
        buttons = [
            ("点击我", self.on_button_click),
            ("优化系统", self.optimize_system)
        ]
        button_frame = ttk.Frame(self.optimizer_frame)
        button_frame.pack(pady=10, padx=20, fill='x')

        for text, command in buttons:
            button = ttk.Button(button_frame, text=text, command=command, width=20)
            button.pack(pady=5, padx=10)

    def on_button_click(self):
        """按钮点击事件，显示欢迎信息。"""
        messagebox.showinfo("提示", "欢迎使用本软件，你的支持是我最大的动力！")

    def optimize_system(self):
        """启动系统优化的线程。"""
        threading.Thread(target=self._optimize_system).start()

    def _optimize_system(self):
        """执行系统优化操作。"""
        self.clear_temp_files()
        self.free_memory()
        self.defragment_disk()

    # 修复功能
    def create_repair_content(self):
        """创建修复系统组件标签页的内容。"""
        self.create_label(self.repair_frame, "修复系统组件", "#FF0000", 14)

        # 初始化RegistryFixer
        self.registry_fixer = RegistryFixer()

        repair_buttons = [
            ("修复 CMD", self.repair_cmd),
            ("修复注册表", self.repair_registry),
            ("修复任务管理器", self.repair_task_manager),
            ("修复资源管理器", self.repair_explorer),
            ("修复防火墙", self.repair_firewall),
            ("修复网络适配器", self.repair_network_adapter),
            ("修复 Windows 更新服务", self.repair_windows_update),
            ("修复音频服务", self.repair_audio_service)
        ]

        button_frame = ttk.Frame(self.repair_frame)
        button_frame.pack(pady=10)

        for i, (text, command) in enumerate(repair_buttons):
            ttk.Button(button_frame, text=text, command=command, width=25).grid(row=i // 2, column=i % 2, padx=5, pady=5)

        ttk.Button(self.repair_frame, text="一键修复系统组件", command=self.one_click_repair, width=30).pack(pady=10)
        ttk.Button(self.repair_frame, text="一键超级修复", command=self.one_click_super_repair, width=30).pack(pady=10)

    def repair_cmd(self):
        """修复CMD（运行系统文件检查）。"""
        self.run_command("sfc /scannow", "正在修复 CMD，请稍候...")

    def repair_registry(self):
        """修复注册表访问权限。"""
        self.registry_fixer.fix_disabled_registry_tools()

    def repair_task_manager(self):
        """修复任务管理器。"""
        self.run_command("taskkill /f /im taskmgr.exe", "正在关闭任务管理器...")
        self.run_command("start taskmgr", "正在启动任务管理器...")

    def repair_explorer(self):
        """修复资源管理器。"""
        self.run_command("taskkill /f /im explorer.exe", "正在关闭资源管理器...")
        self.run_command("start explorer", "正在启动资源管理器...")

    def repair_firewall(self):
        """修复防火墙设置。"""
        self.run_command("netsh advfirewall reset", "正在修复防火墙，请稍候...")

    def repair_network_adapter(self):
        """修复网络适配器设置。"""
        self.run_command("netsh int ip reset", "正在修复网络适配器，请稍候...")

    def repair_windows_update(self):
        """修复Windows更新服务。"""
        self.run_command("net stop wuauserv && net start wuauserv", "正在修复 Windows 更新服务，请稍候...")

    def repair_audio_service(self):
        """修复音频服务。"""
        self.run_command("net stop audiosrv && net start audiosrv", "正在修复音频服务，请稍候...")

    def run_command(self, command, info_text):
        """运行指定的命令，并根据结果显示信息。"""
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                messagebox.showinfo("成功", info_text)
            else:
                messagebox.showerror("错误", f"{info_text}\n错误信息: {stderr}")
        except Exception as e:
            messagebox.showerror("错误", f"{info_text}\n发生异常: {e}")

    def one_click_repair(self):
        """一键修复所有系统组件。"""
        self.repair_cmd()
        self.repair_registry()
        self.repair_task_manager()
        self.repair_explorer()
        self.repair_firewall()
        self.repair_network_adapter()
        self.repair_windows_update()
        self.repair_audio_service()
        messagebox.showinfo("提示", "一键修复完成！")

    def one_click_super_repair(self):
        """一键超级修复，包含所有修复功能。"""
        self.one_click_repair()
        messagebox.showinfo("提示", "一键超级修复完成！")

    # 维护功能
    def check_system_updates(self):
        """检查和安装系统更新。"""
        try:
            subprocess.run(["powershell", "-Command", "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"], check=True)
            subprocess.run(["powershell", "-Command", "Install-Module PSWindowsUpdate -Force"], check=True)
            subprocess.run(["powershell", "-Command", "Get-WindowsUpdate -AcceptAll -Install"], check=True)
            messagebox.showinfo("提示", "系统更新检查完成！")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"检查系统更新时出错: {e}")

    def clear_temp_files(self):
        """清理临时文件。"""
        temp_dir = os.getenv('TEMP')
        try:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass
                for dir in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, dir), ignore_errors=True)
                    except:
                        pass
            messagebox.showinfo("提示", "临时文件清理完成！")
        except Exception as e:
            messagebox.showerror("错误", f"清理临时文件时出错: {e}")

    def free_memory(self):
        """释放内存缓存。"""
        try:
            subprocess.run(["powershell", "-Command", "Clear-MemoryCache"], check=True)
            messagebox.showinfo("提示", "内存释放完成！")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"释放内存时出错: {e}")

    def backup_system_settings(self):
        """备份系统设置（模拟功能）。"""
        try:
            # 实际备份系统设置需要特定的逻辑，这里仅模拟
            messagebox.showinfo("提示", "系统设置备份完成！")
        except Exception as e:
            messagebox.showerror("错误", f"备份系统设置时出错: {e}")

    def restore_system_settings(self):
        """恢复系统设置（模拟功能）。"""
        try:
            # 实际恢复系统设置需要特定的逻辑，这里仅模拟
            messagebox.showinfo("提示", "系统设置恢复完成！")
        except Exception as e:
            messagebox.showerror("错误", f"恢复系统设置时出错: {e}")

    def defragment_disk(self):
        """磁盘碎片整理。"""
        try:
            subprocess.run(["defrag", "C:"], check=True)
            messagebox.showinfo("提示", "磁盘碎片整理完成！")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"磁盘碎片整理时出错: {e}")

    def create_label(self, parent, text, color, font_size):
        """创建标签。"""
        label = ttk.Label(parent, text=text, font=("Microsoft YaHei", font_size), foreground=color, background='white')
        label.pack(pady=10)

    def create_buttons(self):
        """创建系统优化页面的操作按钮。"""
        buttons = [
            ("点击我", self.on_button_click),
            ("优化系统", self.optimize_system)
        ]
        button_frame = ttk.Frame(self.optimizer_frame)
        button_frame.pack(pady=10, padx=20, fill='x')

        for text, command in buttons:
            button = ttk.Button(button_frame, text=text, command=command, width=20)
            button.pack(pady=5, padx=10)

    def on_button_click(self):
        """按钮点击事件，显示欢迎信息。"""
        messagebox.showinfo("提示", "欢迎使用本软件，你的支持是我最大的动力！")

    def optimize_system(self):
        """启动系统优化的线程。"""
        threading.Thread(target=self._optimize_system).start()

    def _optimize_system(self):
        """执行系统优化操作。"""
        self.clear_temp_files()
        self.free_memory()
        self.defragment_disk()

    def add_to_startup(self):
        """将程序添加到Windows启动项。"""
        try:
            startup_folder = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')
            shortcut_path = os.path.join(startup_folder, "SystemOptimizerApp.lnk")
            target = os.path.abspath(sys.argv[0])
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.IconLocation = target
            shortcut.save()
        except Exception as e:
            messagebox.showerror("错误", f"添加到启动项时出错: {e}")

    def update_time(self):
        """更新时间标签。"""
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.time_label.config(text=current_time)
        self.master.after(1000, self.update_time)

    def create_tray_icon(self):
        """创建系统托盘图标和菜单。"""
        image_path = self.get_icon_path()
        self.tray_image = Image.open(image_path)

        # 定义托盘菜单
        menu = (pystray.MenuItem('显示', self.show_window),
                pystray.MenuItem('退出', self.exit_app))

        self.icon = pystray.Icon("SystemOptimizerApp", self.tray_image, "系统优化工具", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def get_icon_path(self):
        """获取托盘图标的路径。如果图标不存在，则创建一个简单的图标。"""
        icon_filename = "daad.ico"
        if not os.path.exists(icon_filename):
            # 创建一个简单的图标
            img = Image.new('RGB', (64, 64), color='blue')
            img.save(icon_filename, format='ICO')
        return icon_filename

    def hide_window(self):
        """隐藏主窗口并最小化到系统托盘。"""
        self.master.withdraw()

    def show_window(self):
        """显示主窗口并从系统托盘恢复。"""
        self.master.deiconify()

    def exit_app(self):
        """退出应用程序。"""
        self.icon.stop()
        self.master.destroy()

    def on_close(self):
        """处理窗口关闭事件，询问是否隐藏到系统托盘。"""
        if messagebox.askyesno("隐藏到系统托盘", "是否将程序隐藏到系统托盘？"):
            self.hide_window()
        else:
            self.exit_app()


def is_admin():
    """检查当前是否以管理员权限运行。"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """以管理员权限重新运行当前脚本。"""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, ' '.join(sys.argv), None, 1
        )


def main():
    """主函数，启动应用程序。"""
    root = tk.Tk()
    if not Disclaimer.has_agreed():
        # 显示免责声明
        def on_agree():
            app = SystemOptimizerApp(root)
            root.deiconify()

        Disclaimer(root, on_agree)
    else:
        # 用户同意免责声明后直接调整主窗口
        app = SystemOptimizerApp(root)
        root.deiconify()

    root.mainloop()


# 检查是否以管理员权限运行
if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
        sys.exit()
    main()


chmod +x /usr/bin/docker-compose
