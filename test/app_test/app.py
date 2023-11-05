import tkinter as tk
import threading
import subprocess

# 定义函数来运行脚本1
def run_script1():
    # 禁用按钮1
    button1.config(state=tk.DISABLED)
    
    # 显示交互信息
    info_label1.config(text="正在监听中，请勿重复点击···")
    
    # 启动脚本1的线程
    script_thread = threading.Thread(target=run_script, args=("scripts/script1.py",))
    script_thread.start()

# 定义函数来运行脚本2
def run_script2():
    # 禁用按钮2
    button2.config(state=tk.DISABLED)
    
    # 显示交互信息
    info_label2.config(text="生成报告中，请勿重复点击···")
    
    # 启动脚本2的线程
    script_thread = threading.Thread(target=run_script, args=("scripts/script2.py",))
    script_thread.start()

# 定义函数来运行脚本
def run_script(script_name):
    # 启动脚本
    subprocess.Popen(["python", script_name], shell=True).wait()
    
    # 恢复按钮的状态
    if script_name == "scripts/script1.py":
        button1.config(state=tk.NORMAL)
        info_label1.config(text="")
    elif script_name == "scripts/script2.py":
        button2.config(state=tk.NORMAL)
        info_label2.config(text="")

# 创建主窗口
root = tk.Tk()
root.title("智能台灯")

# 放大窗口的大小
root.geometry("400x300")

# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口居于屏幕中间的位置
x = (screen_width - 400) // 2  # 窗口宽度
y = (screen_height - 300) // 2  # 窗口高度

# 设置窗口位置
root.geometry(f"400x300+{x}+{y}")

# 添加主标题
title_label = tk.Label(root, text="智能台灯", font=("微软雅黑", 16))
title_label.pack()

# 创建按钮1和相应的标签
button1 = tk.Button(root, text="开始监听", command=run_script1, font=("微软雅黑", 12))
button1.pack()
info_label1 = tk.Label(root, text="", font=("微软雅黑", 12))
info_label1.pack()

# 创建按钮2和相应的标签
button2 = tk.Button(root, text="生成报告", command=run_script2, font=("微软雅黑", 12))
button2.pack()
info_label2 = tk.Label(root, text="", font=("微软雅黑", 12))
info_label2.pack()

# 启动GUI主循环
root.mainloop()
