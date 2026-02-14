import tkinter as tk
import subprocess
import webbrowser
import sys
import os

# 添加获取资源文件路径的函数
def resource_path(relative_path):
    """ 获取资源文件的绝对路径 """
    try:
        # PyInstaller 创建临时文件夹，并将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class StartupGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和尺寸
        self.root.title('RWMP2_Decryptor2.2.0')
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f2f5')
        
        # 添加窗口图标设置 - 使用资源路径函数
        icon_path = resource_path('icon.ico')
        try:
            self.root.iconbitmap(icon_path)
        except:
            pass  # 如果图标文件不存在则忽略

        # 标题标签
        title = tk.Label(
            self.root,
            text='开源的铁锈模组解密器\n官网:https://coralhymn.com \nGithub:https://github.com/CoralHymn/RWMP2_Decryptor',
            font=('Arial', 14),
            fg='#2b2d42',
            bg='#f0f2f5',
            justify=tk.CENTER
        )
        title.pack(pady=20)

        # 勾选框变量
        self.agreement_var = tk.BooleanVar(value=True)

        # 勾选框及其文字
        agreement_frame = tk.Frame(self.root, bg='#f0f2f5')
        agreement_frame.pack(pady=10)

        agreement_check = tk.Checkbutton(
            agreement_frame,
            text='我已阅读',
            variable=self.agreement_var,
            bg='#f0f2f5',
            font=('Arial', 12),
            command=self.toggle_buttons
        )
        agreement_check.pack(side=tk.LEFT)

        # 使用教程链接
        tutorial_link = tk.Label(
            agreement_frame,
            text='使用教程',
            fg='blue',
            cursor='hand2',
            bg='#f0f2f5',
            font=('Arial', 12, 'underline')
        )
        tutorial_link.pack(side=tk.LEFT, padx=5)
        tutorial_link.bind("<Button-1>", lambda e: webbrowser.open("https://cc00.top"))

        # 使用条款链接
        terms_link = tk.Label(
            agreement_frame,
            text='与使用条款',
            fg='blue',
            cursor='hand2',
            bg='#f0f2f5',
            font=('Arial', 12, 'underline')
        )
        terms_link.pack(side=tk.LEFT, padx=5)
        terms_link.bind("<Button-1>", lambda e: webbrowser.open("https://cc00.top"))

        # 按钮框架
        button_frame = tk.Frame(self.root, bg='#f0f2f5')
        button_frame.pack(pady=20)

        # GUI版本按钮
        self.gui_button = tk.Button(
            button_frame,
            text='使用GUI版本',
            command=self.run_gui_version,
            bg='#4361ee',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            state=tk.NORMAL if self.agreement_var.get() else tk.DISABLED
        )
        self.gui_button.pack(side=tk.LEFT, padx=10)

        # WEB版本按钮
        self.web_button = tk.Button(
            button_frame,
            text='使用WEB版本',
            command=self.run_web_version,
            bg='#2a9d8f',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            state=tk.NORMAL if self.agreement_var.get() else tk.DISABLED
        )
        self.web_button.pack(side=tk.LEFT, padx=10)

    def toggle_buttons(self):
        """根据勾选框状态启用或禁用按钮"""
        state = tk.NORMAL if self.agreement_var.get() else tk.DISABLED
        self.gui_button.config(state=state)
        self.web_button.config(state=state)

    def run_gui_version(self):
        """运行GUI版本"""
        try:
            # 直接导入并运行GUI，而不是启动新进程
            from gui_wrapper import ModernGUI
            self.root.withdraw()  # 隐藏启动窗口
            try:
                window = ModernGUI()
                window.show()
            finally:
                self.root.deiconify()  # 重新显示启动窗口
        except Exception as e:
            tk.messagebox.showerror("错误", f"无法启动GUI版本: {e}")

    def run_web_version(self):
        """运行Web版本"""
        try:
            # 直接导入并运行Web版本，而不是启动新进程
            from RWMP2_Decryptor_Web import web_main
            import threading
            
            # 在新线程中启动web服务器，避免阻塞GUI
            def start_web_server():
                try:
                    print("正在启动Web服务器... 访问 http://localhost:8085")
                    from pywebio import start_server
                    start_server(web_main, port=8085, debug=True, host='localhost', auto_open_webbrowser=True)
                except Exception as e:
                    print(f"启动Web服务器失败: {e}")
            
            web_thread = threading.Thread(target=start_web_server, daemon=True)
            web_thread.start()
            
        except Exception as e:
            tk.messagebox.showerror("错误", f"无法启动Web版本: {e}")

    def show(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = StartupGUI()
    app.show()