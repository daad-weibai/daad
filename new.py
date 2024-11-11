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
from win.Disclaimer import Disclaimer

# 本程序由daad开发
# 本程序受著作权法保护

if __name__ == '__main__':
    disclaimer = Disclaimer()
    if disclaimer.flag:
        pass

