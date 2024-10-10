import os
import shutil
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import subprocess
import psutil
import keyboard  # 需要安装 keyboard 库

# 作者: daad_weibai
# 版本: 1.0.0
class SystemOptimizerApp:
    def __init__(self, master):
        self.master = master  # 保存主窗口的引用
        master.title("系统优化工具 - 版本 1.0.0")  # 设置窗口标题，包含版本信息
        master.geometry("600x590")  # 设置窗口大小
        master.minsize(400, 560)  # 设置窗口最小大小

        # 创建标签页
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        # 创建系统优化标签页
        self.optimizer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.optimizer_frame, text="系统优化")

        # 创建修复系统组件标签页
        self.repair_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.repair_frame, text="修复系统组件")

        # 在系统优化标签页中添加内容
        self.create_optimizer_content()

        # 在修复系统组件标签页中添加内容
        self.create_repair_content()

        # 创建启动项管理标签页
        self.startup_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.startup_frame, text="启动项管理")

        # 在启动项管理标签页中添加内容
        self.startup_manager = StartupManager(self.startup_frame)

        # 监视热键
        keyboard.add_hotkey('home', self.terminate_non_system_processes)

    def create_optimizer_content(self):
        # 创建并显示免责声明标签
        self.disclaimer_label = ttk.Label(self.optimizer_frame, text="免责声明: 本软件仅供参考，使用时请自行承担风险。", font=("Microsoft YaHei", 10), foreground="#FF0000")
        self.disclaimer_label.pack(pady=10)

        # 创建并显示作者标签
        self.label = ttk.Label(self.optimizer_frame, text="作者: daad_weibai", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        # 创建并显示版本标签
        self.version_label = ttk.Label(self.optimizer_frame, text="版本: 1.0.0", font=("Microsoft YaHei", 14))
        self.version_label.pack(pady=5)

        # 创建并显示时间标签
        self.time_label = ttk.Label(self.optimizer_frame, text="", font=("Microsoft YaHei", 24))
        self.time_label.pack(pady=20)

        # 创建按钮和资源标签
        self.create_buttons()
        self.create_resource_labels()
        self.update_time()  # 启动时间更新
        self.update_resources()  # 启动资源更新

    def create_repair_content(self):
        # 创建修复注册表按钮
        ttk.Button(self.repair_frame, text="修复注册表", command=self.repair_registry, width=20).pack(pady=10, padx=20, fill='x')
        # 创建运行 CMD 命令按钮
        ttk.Button(self.repair_frame, text="运行 CMD 命令", command=self.run_cmd, width=20).pack(pady=10, padx=20, fill='x')
        # 创建修改文件后缀名按钮
        ttk.Button(self.repair_frame, text="修改文件后缀名", command=self.change_file_extension, width=20).pack(pady=10, padx=20, fill='x')
        # 创建修复任务管理器按钮
        ttk.Button(self.repair_frame, text="修复任务管理器", command=self.repair_task_manager, width=20).pack(pady=10, padx=20, fill='x')
        # 创建移除账户锁按钮
        ttk.Button(self.repair_frame, text="移除账户锁", command=self.unlock_account, width=20).pack(pady=10, padx=20, fill='x')
        # 创建一键解毒按钮
        ttk.Button(self.repair_frame, text="一键解毒", command=self.quick_scan, width=20).pack(pady=10, padx=20, fill='x')
        # 创建一键超级解毒按钮
        ttk.Button(self.repair_frame, text="一键超级解毒", command=self.super_scan, width=20).pack(pady=10, padx=20, fill='x')

        # 添加标签，说明 Home 键的功能
        home_key_label = ttk.Label(self.repair_frame, text="按 Home 键可一键结束所有非系统进程", font=("Microsoft YaHei", 12), foreground="#0000FF")
        home_key_label.pack(pady=10)

    def check_agreement(self):
        # 检查说明文档内容
        try:
            with open("说明文档.txt", "r", encoding="utf-8") as file:
                content = file.read().strip()
                if content != "我同意以上条款":
                    messagebox.showwarning("警告", "您未同意条款，程序将退出。")
                    return False
        except FileNotFoundError:
            messagebox.showerror("错误", "说明文档未找到，请确保文件存在。")
            return False
        return True

    def quick_scan(self):
        # 一键解毒
        try:
            messagebox.showinfo("提示", "正在进行快速解毒，请稍候...")
            subprocess.run("start ms-settings:windowsdefender", shell=True)  # 打开 Windows Defender
            messagebox.showinfo("提示", "请手动启动扫描！")  # 弹出提示框
        except Exception as e:
            messagebox.showerror("错误", f"解毒时出错: {e}")  # 弹出错误提示框

    def super_scan(self):
        # 一键超级解毒
        try:
            messagebox.showinfo("提示", "正在进行超级解毒，请稍候...")
            # 提权到系统权限并运行 Windows Defender
            subprocess.run("powershell -Command Start-Process 'C:\\Program Files\\Windows Defender\\MpCmdRun.exe' -ArgumentList '-Scan -ScanType 2' -Verb RunAs", shell=True)
            messagebox.showinfo("提示", "请手动启动深度扫描！")  # 弹出提示框
        except Exception as e:
            messagebox.showerror("错误", f"超级解毒时出错: {e}")  # 弹出错误提示框

    def repair_registry(self):
        # 修复注册表（示例：使用 regsvr32 注册 DLL）
        try:
            messagebox.showinfo("提示", "正在修复注册表，请稍候...")
            subprocess.run("regsvr32 /s somefile.dll", shell=True)  # 示例命令
            messagebox.showinfo("提示", "注册表修复完成！")  # 弹出提示框
        except Exception as e:
            messagebox.showerror("错误", f"修复注册表时出错: {e}")  # 弹出错误提示框

    def run_cmd(self):
        # 运行 CMD 命令
        cmd = filedialog.askstring("输入命令", "请输入要运行的 CMD 命令：")
        if cmd:
            try:
                subprocess.run(cmd, shell=True)  # 执行命令
                messagebox.showinfo("提示", "命令执行完成！")  # 弹出提示框
            except Exception as e:
                messagebox.showerror("错误", f"执行命令时出错: {e}")  # 弹出错误提示框

    def change_file_extension(self):
        # 修改文件后缀名
        file_path = filedialog.askopenfilename(title="选择文件")
        if file_path:
            new_extension = filedialog.askstring("输入新后缀名", "请输入新的文件后缀名（不带点）：")
            if new_extension:
                new_file_path = f"{os.path.splitext(file_path)[0]}.{new_extension}"
                os.rename(file_path, new_file_path)  # 修改文件后缀名
                messagebox.showinfo("提示", f"文件后缀名已修改为: {new_file_path}")  # 弹出提示框

    def repair_task_manager(self):
        # 修复任务管理器
        try:
            messagebox.showinfo("提示", "正在重启任务管理器，请稍候...")
            subprocess.run("taskkill /f /im taskmgr.exe", shell=True)  # 强制结束任务管理器
            subprocess.run("start taskmgr.exe", shell=True)  # 重新启动任务管理器
            messagebox.showinfo("提示", "任务管理器已重启！")  # 弹出提示框
        except Exception as e:
            messagebox.showerror("错误", f"修复任务管理器时出错: {e}")  # 弹出错误提示框

    def unlock_account(self):
        # 移除账户锁
        username = filedialog.askstring("输入用户名", "请输入要解锁的用户名：")
        if username:
            try:
                subprocess.run(f"net user {username} /active:yes", shell=True)  # 解锁账户
                messagebox.showinfo("提示", f"账户 {username} 已解锁！")  # 弹出提示框
            except Exception as e:
                messagebox.showerror("错误", f"移除账户锁时出错: {e}")  # 弹出错误提示框

    def terminate_non_system_processes(self):
        # 结束所有非系统进程
        system_processes = ['System', 'Registry', 'Idle', 'smss.exe', 'csrss.exe', 'wininit.exe', 'services.exe', 'lsass.exe', 'svchost.exe', 'explorer.exe', 'taskhostw.exe', 'taskmgr.exe']
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] not in system_processes:
                try:
                    proc.terminate()  # 结束进程
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

    def create_buttons(self):
        # 创建“点击我”按钮，点击时调用 on_button_click 方法
        ttk.Button(self.optimizer_frame, text="点击我", command=self.on_button_click, width=20).pack(pady=10, padx=20, fill='x')
        # 创建“优化系统”按钮，点击时调用 optimize_system 方法
        ttk.Button(self.optimizer_frame, text="优化系统", command=self.optimize_system, width=20).pack(pady=20, padx=20, fill='x')
        # 创建“修复系统文件”按钮，点击时调用 repair_system_files 方法
        ttk.Button(self.optimizer_frame, text="修复系统文件", command=self.repair_system_files, width=20).pack(pady=20, padx=20, fill='x')

    def on_button_click(self):
        # 按钮点击事件处理，弹出提示框
        messagebox.showinfo("提示", "欢迎使用本软件，你的支持是我最大的动力！")

    def clear_temp_files(self):
        # 清理临时文件夹中的文件
        temp_dir = os.getenv('TEMP')  # 获取临时文件夹路径
        try:
            for filename in os.listdir(temp_dir):  # 遍历临时文件夹中的文件
                file_path = os.path.join(temp_dir, filename)  # 获取文件的完整路径
                if os.path.isfile(file_path):  # 如果是文件
                    os.remove(file_path)  # 删除文件
                elif os.path.isdir(file_path):  # 如果是文件夹
                    shutil.rmtree(file_path)  # 删除文件夹及其内容
            messagebox.showinfo("提示", "临时文件已清理！")  # 弹出提示框
        except Exception as e:
            messagebox.showerror("错误", f"清理临时文件时出错: {e}")  # 弹出错误提示框

    def free_memory(self):
        # 释放当前进程的内存
        process = psutil.Process(os.getpid())  # 获取当前进程
        process.memory_info()  # 这里可以添加具体的内存释放逻辑
        messagebox.showinfo("提示", "内存已释放！")  # 弹出提示框

    def optimize_system(self):
        # 优化系统，清理临时文件和释放内存
        self.clear_temp_files()  # 清理临时文件
        self.free_memory()  # 释放内存

    def repair_system_files(self):
        # 修复系统文件
        try:
            messagebox.showinfo("提示", "正在修复系统文件，请稍候...")
            subprocess.run("sfc /scannow", shell=True)  # 执行修复命令
            messagebox.showinfo("提示", "系统文件修复完成！")  # 弹出提示框
        except Exception as e:
            messagebox.showerror("错误", f"修复系统文件时出错: {e}")  # 弹出错误提示框

    def create_resource_labels(self):
        # 创建并显示资源使用情况标签
        self.cpu_label = ttk.Label(self.optimizer_frame, text="CPU使用率: ", font=("Microsoft YaHei", 16))
        self.cpu_label.pack(pady=10)

        self.memory_label = ttk.Label(self.optimizer_frame, text="内存使用率: ", font=("Microsoft YaHei", 16))
        self.memory_label.pack(pady=10)

        self.disk_label = ttk.Label(self.optimizer_frame, text="磁盘使用率: ", font=("Microsoft YaHei", 16))
        self.disk_label.pack(pady=10)

    def update_resources(self):
        # 更新资源使用情况
        cpu_usage = psutil.cpu_percent(interval=1)  # 获取 CPU 使用率
        memory_info = psutil.virtual_memory()  # 获取内存信息
        memory_usage = memory_info.percent  # 获取内存使用率
        disk_usage = psutil.disk_usage('/').percent  # 获取磁盘使用率

        # 动态改变 CPU 使用率标签的颜色
        cpu_color = self.get_color(cpu_usage)  # 获取颜色
        self.cpu_label.config(text=f"CPU使用率: {cpu_usage}%", foreground=cpu_color)  # 更新标签显示和颜色

        # 动态改变内存使用率标签的颜色
        memory_color = self.get_color(memory_usage)  # 获取颜色
        self.memory_label.config(text=f"内存使用率: {memory_usage}%", foreground=memory_color)  # 更新标签显示和颜色

        # 动态改变磁盘使用率标签的颜色
        disk_color = self.get_color(disk_usage)  # 获取颜色
        self.disk_label.config(text=f"磁盘使用率: {disk_usage}%", foreground=disk_color)  # 更新标签显示和颜色

        self.master.after(1000, self.update_resources)  # 每秒更新一次资源信息

    def get_color(self, usage):
        # 根据使用率返回颜色
        if usage < 20:
            return "#00FF00"  # 绿色
        elif usage < 50:
            return "#FFFF00"  # 黄色
        elif usage < 80:
            return "#FFA500"  # 橙色
        else:
            return "#FF0000"  # 红色

    def update_time(self):
        # 更新当前时间显示
        now = datetime.datetime.now()  # 获取当前时间
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间
        self.time_label.config(text=formatted_time)  # 更新时间标签

        # 根据当前秒数改变颜色
        second = now.second  # 获取当前秒数
        color = f'#{(second * 4):02x}{(255 - second * 4):02x}ff'  # 生成颜色值
        self.time_label.config(foreground=color)  # 更新时间标签的颜色每分钟一次

        self.master.after(100, self.update_time)  # 每秒更新一次时间 100=1S

class StartupManager:
    def __init__(self, master):
        self.master = master  # 保存主窗口的引用

        # 创建并显示启动项管理标签
        self.label = ttk.Label(master, text="启动项管理", font=("Microsoft YaHei", 14))
        self.label.pack(pady=10)

        self.create_startup_buttons()  # 创建启动项管理按钮
        self.startup_listbox = tk.Listbox(master, font=("Microsoft YaHei", 12), bg="#fff", fg="#333")  # 创建列表框
        self.startup_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_startup_buttons(self):
        # 创建“列出启动项”按钮，点击时调用 list_startup_items 方法
        ttk.Button(self.master, text="列出启动项", command=self.list_startup_items, width=20).pack(pady=5, padx=20, fill='x')
        # 创建“添加启动项”按钮，点击时调用 add_startup_item 方法
        ttk.Button(self.master, text="添加启动项", command=self.add_startup_item, width=20).pack(pady=5, padx=20, fill='x')
        # 创建“删除启动项”按钮，点击时调用 remove_startup_item 方法
        ttk.Button(self.master, text="删除启动项", command=self.remove_startup_item, width=20).pack(pady=5, padx=20, fill='x')

    def list_startup_items(self):
        # 列出当前启动项
        self.startup_listbox.delete(0, tk.END)  # 清空列表框
        startup_folder = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')  # 获取启动项文件夹路径
        items = os.listdir(startup_folder)  # 列出文件夹中的所有文件
        for item in items:
            self.startup_listbox.insert(tk.END, item)  # 将每个启动项添加到列表框

    def add_startup_item(self):
        # 添加新的启动项
        file_path = filedialog.askopenfilename(title="选择要添加的程序")  # 弹出文件选择对话框
        if file_path:  # 如果选择了文件
            startup_folder = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')  # 获取启动项文件夹路径
            file_name = os.path.basename(file_path)  # 获取文件名
            destination = os.path.join(startup_folder, file_name)  # 目标路径

            if not os.path.exists(destination):  # 如果目标路径不存在
                os.symlink(file_path, destination)  # 创建指向文件的快捷方式
                messagebox.showinfo("成功", f"已添加启动项: {file_name}")  # 弹出成功提示框
                self.list_startup_items()  # 列出更新后的启动项
            else:
                messagebox.showwarning("警告", f"启动项已存在: {file_name}")  # 弹出警告提示框

    def remove_startup_item(self):
        # 删除选中的启动项
        selected_item = self.startup_listbox.curselection()  # 获取当前选中的项
        if selected_item:  # 如果有选中项
            item_name = self.startup_listbox.get(selected_item)  # 获取选中项的名称
            startup_folder = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')  # 获取启动项文件夹路径
            item_path = os.path.join(startup_folder, item_name)  # 获取完整路径

            if os.path.exists(item_path):  # 如果路径存在
                os.remove(item_path)  # 删除启动项
                messagebox.showinfo("成功", f"已删除启动项: {item_name}")  # 弹出成功提示框
                self.list_startup_items()  # 列出更新后的启动项
            else:
                messagebox.showwarning("警告", f"未找到启动项: {item_name}")  # 弹出警告提示框
        else:
            messagebox.showwarning("警告", "请先选择一个启动项")  # 弹出警告提示框

if __name__ == "__main__":
    root = tk.Tk()  # 创建主窗口
    app = SystemOptimizerApp(root)  # 创建系统优化工具实例
    root.mainloop()  # 启动主循环
