import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
from tkinterdnd2 import TkinterDnD, DND_FILES
import subprocess
import os
import configparser
import time
import sys

class DualApp:
    def __init__(self, root):
        self.root = root
        self.launch_success = False
        self.config = configparser.ConfigParser()
        self.config_folder_path = os.path.join(os.path.expanduser("~"), "双开应用工具")
        if not os.path.exists(self.config_folder_path):
            os.makedirs(self.config_folder_path)
        self.config_file_path = os.path.join(self.config_folder_path, "DualAPP_Config.ini")

        if os.path.exists(self.config_file_path):
            self.config.read(self.config_file_path)
            self.APP_path = self.config.get("Settings", "APPPath")
        else:
            self.APP_path = ""

        self.create_widgets()

    def create_default_config(self):
        self.config["Settings"] = {"APPPath": ""}
        with open(self.config_file_path, "w") as config_file:
            self.config.write(config_file)

    def create_widgets(self):
        self.path_label = tk.Label(self.root, text="请点击选择应用路径，或者将图标拖到此界面。\n当前双开程序路径：\n" + self.APP_path)
        self.path_label.pack(pady=10)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

        self.choose_path_button = tk.Button(self.root, text="选择应用", command=self.choose_path)
        self.choose_path_button.pack(pady=10)

        self.launch_button = tk.Button(self.root, text="双开应用", command=self.launch_APP)
        self.launch_button.pack(pady=10)

        self.root.after(100, self.check_launch_success)

    def save_config(self):
        self.config["Settings"] = {"APPPath": self.APP_path}
        with open(self.config_file_path, "w") as ConfigFile:
            self.config.write(ConfigFile)

    def launch_APP(self):
        # 如果用户未输入路径，提示用户选择应用程序路径
        if not self.APP_path:
            self.APP_path = filedialog.askopenfilename(title="选择exe文件", filetypes=[("执行文件", "*.exe")])

            # 用户取消选择，直接返回
            if not self.APP_path:
                return

            self.save_config()

        try:
            # 启动两次应用
            subprocess.Popen([self.APP_path], cwd=os.path.dirname(self.APP_path), shell=True)
            subprocess.Popen([self.APP_path], cwd=os.path.dirname(self.APP_path), shell=True)
            self.launch_success = True
        except Exception as e:
            self.launch_success = False
            # 弹出错误提示框
            messagebox.showerror("启动失败", f"无法启动应用程序：{str(e)}")

    def exit_program(self):
        time.sleep(1)
        sys.exit()

    def check_launch_success(self):
        if self.launch_success:
            self.temp_path = ""
            self.exit_program()
        self.root.after(150, self.check_launch_success)

    def on_drop(self, event):
        self.temp_path = event.data
        self.check_path()
        self.APP_path = self.temp_path
        self.path_label.config(text="请点击选择应用路径，或者将图标拖到此界面。\n当前双开程序路径：\n" + self.APP_path)
        self.save_config()

    def process_string(self, input_str):
        if len(input_str) == 0:
            return input_str

        if input_str[0] == '{' and input_str[-1] == '}':
            return input_str[1:-1]
        else:
            return input_str
    
    def is_valid_file_path(self):  
        self.temp_path = self.process_string(self.temp_path)
        try:
            if not os.path.exists(self.temp_path):
                return f"路径'{self.temp_path}'不存在。"
            if not os.path.isfile(self.temp_path):
                return f"'{self.temp_path}'不是一个文件。"
            _, file_extension = os.path.splitext(self.temp_path)
            if file_extension.lower() not in ('.exe', '.lnk'):
                return f"'{self.temp_path}'不是应用程序。"
            return None
        except Exception as e:
            return f"发生异常：{e}"

    def check_path(self):
        error_message = self.is_valid_file_path()
        if error_message:
            self.temp_path = ""
            messagebox.showerror("错误", error_message)

    def choose_path(self):
        self.APP_path = filedialog.askopenfilename(title="选择exe文件", filetypes=[("执行文件", "*.exe")])
        self.path_label.config(text="请点击选择应用路径，或者将图标拖到此界面。\n当前双开程序路径：\n" + self.APP_path)
        self.save_config()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("双开应用")
    root.geometry("400x200")
    root.resizable(width=False, height=False)
    app = DualApp(root)
    root.mainloop()
