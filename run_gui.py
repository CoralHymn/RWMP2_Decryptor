import tkinter as tk
import subprocess
import webbrowser

class StartupGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和尺寸
        self.root.title('RWMP2_Decryptor2.1.0')
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f2f5')

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
            subprocess.Popen(['python', 'gui_wrapper.py'])
            self.root.destroy()  # 成功运行后关闭当前窗口
        except Exception as e:
            tk.messagebox.showerror("错误", f"无法启动GUI版本: {e}")

    def run_web_version(self):
        """运行Web版本"""
        try:
            subprocess.Popen(['python', 'RWMP2_Decryptor_Web.py'])
            self.root.destroy()  # 成功运行后关闭当前窗口
        except Exception as e:
            tk.messagebox.showerror("错误", f"无法启动Web版本: {e}")

    def show(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = StartupGUI()
    app.show()