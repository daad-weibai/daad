import os
import sys
import tkinter as tk


class Disclaimer:
    """免责声明窗口，用户首次运行时显示，并记录用户同意情况。"""

    def __init__(self):
        self.flag = self.has_agreed()
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口

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

        self.label = tk.Label(self.disclaimer_window, text=disclaimer_text, wraplength=580, justify="left"
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
        self.root.mainloop()

    def agree(self):
        """用户同意免责声明后记录并显示主窗口。"""
        # 创建一个文件以记录用户已同意免责声明
        with open(self.get_disclaimer_file_path(), "w") as f:
            f.write("Agreed")
        self.disclaimer_window.destroy()
        # self.on_agree_callback()  # 回调函数显示主窗口

    def disagree(self):
        """用户不同意免责声明后关闭主程序。"""
        self.root.destroy()  # 关闭主程序
        sys.exit()

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


if __name__ == '__main__':
    Disclaimer()
