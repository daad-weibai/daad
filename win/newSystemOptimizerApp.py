import os
import threading
from tkinter import ttk, messagebox

import pystray
from PIL import Image


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
            ttk.Button(button_frame, text=text, command=command, width=25).grid(row=i // 2, column=i % 2, padx=5,
                                                                                pady=5)

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
            subprocess.run(["powershell", "-Command", "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"],
                           check=True)
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
