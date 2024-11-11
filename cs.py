# import tkinter as tk
#
# root = tk.Tk()
# root.geometry("400x300")
#
# # 创建三个 Frame，分别填充不同的颜色
# frame1 = tk.Frame(root, bg="red")
# frame2 = tk.Frame(root, bg="green")
# frame3 = tk.Frame(root, bg="blue", height=10)
#
# # 使用 pack 布局管理器，设置 fill=tk.BOTH 和 expand=True
# frame1.pack(fill=tk.BOTH,expand=True)
# frame2.pack(fill=tk.BOTH)
# frame3.pack(fill=tk.BOTH)
#
# root.mainloop()
import tkinter as tk

root = tk.Tk()
frame = tk.Frame(root, borderwidth=2, relief="groove")
frame.pack()

label = tk.Label(frame, text="This is a label inside a frame")
label.pack(pady=10)

root.mainloop()