import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading


from RWMP2_Decryptor import reverse_replace_in_zip, AdvancedZipRepair

class WorkerThread(threading.Thread):
    """一个在后台运行原修复脚本的线程"""
    def __init__(self, zip_path, log_callback, finished_callback):
        super().__init__()
        self.zip_path = zip_path
        self.log_callback = log_callback
        self.finished_callback = finished_callback

    def run(self):
        try:
            self.log_callback("第一步：执行逆向替换预处理...")
            processed_data = reverse_replace_in_zip(self.zip_path)

            self.log_callback("\n第二步：开始修复ZIP文件...")
            repair_tool = AdvancedZipRepair(self.zip_path, processed_data)
            # 重定向原脚本的print输出到GUI
            import builtins
            original_print = builtins.print

            def gui_print(*args, **kwargs):
                msg = ' '.join(map(str, args))
                self.log_callback(msg)

            builtins.print = gui_print

            success = repair_tool.repair_zip()

            # 恢复print函数
            builtins.print = original_print

            if success:
                # 尝试找到生成的最终ZIP文件
                stem = os.path.splitext(os.path.basename(self.zip_path))[0]
                final_zip = f"{stem}_最终修复.zip"
                if os.path.exists(final_zip):
                    self.finished_callback(final_zip)
                    self.log_callback(f"\n🎉 处理成功！修复后的文件已生成：{final_zip}")
                else:
                    self.finished_callback("")
                    self.log_callback("\n处理成功，但未找到最终ZIP文件。")
            else:
                self.finished_callback("")
                self.log_callback("\n❌ 处理失败。")

        except Exception as e:
            import traceback
            self.log_callback(f"\n❌ 处理过程中发生严重错误：{str(e)}")
            self.log_callback(traceback.format_exc())
            self.finished_callback("")


class ModernGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.final_zip_path = ""
        self.initUI()

    def initUI(self):
        self.root.title('RWMP2_Decryptor2.0.2')
        self.root.geometry('600x500')
        self.root.minsize(600, 500)
        
        # 设置整体样式
        self.root.configure(bg='#f0f2f5')
        
        # 创建主框架
        main_frame = tk.Frame(self.root, bg='#f0f2f5')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # 标题
        title = tk.Label(main_frame, text='RWMP2 Decryptor GUI', 
                        font=('Segoe UI', 18, 'bold'),
                        fg='#2b2d42', bg='#f0f2f5')
        title.pack(pady=(0, 10))
        
        subtitle = tk.Label(main_frame, 
                           text='开源的铁锈模组解密器\n官网:https://coralhymn.com \nGithub:https://github.com/CoralHymn/RWMP2_Decryptor',
                           font=('Arial', 13),
                           fg='#6c757d', bg='#f0f2f5', justify=tk.CENTER)
        subtitle.pack(pady=(0, 20))
        
        # 文件选择区域
        file_frame = tk.Frame(main_frame, bg='#f0f2f5')
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.file_label = tk.Label(file_frame, text='未选择文件',
                                  relief=tk.RAISED, bd=1,
                                  bg='white', fg='#6c757d',
                                  anchor='w', padx=8, pady=8)
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_select = tk.Button(file_frame, text='选择模组文件',
                              command=self.select_file,
                              bg='#4361ee', fg='white',
                              relief=tk.FLAT, padx=15, pady=10,
                              font=('Arial', 14, 'bold'),
                              cursor='hand2')
        btn_select.pack(side=tk.RIGHT)
        
        # 开始按钮
        self.btn_start = tk.Button(main_frame, text='开始处理',
                                  command=self.start_processing,
                                  bg='#4361ee', fg='white',
                                  relief=tk.FLAT, padx=15, pady=10,
                                  font=('Arial', 14, 'bold'),
                                  state=tk.DISABLED,
                                  cursor='hand2')
        self.btn_start.pack(pady=10)
        
        # 下载区域
        download_frame = tk.Frame(main_frame, bg='#f0f2f5')
        download_frame.pack(fill=tk.X, pady=10)
        
        self.btn_download = tk.Button(download_frame, text='下载处理结果',
                                     command=self.download_file,
                                     bg='#2a9d8f', fg='white',
                                     relief=tk.FLAT, padx=15, pady=10,
                                     font=('Arial', 14, 'bold'),
                                     state=tk.DISABLED,
                                     cursor='hand2')
        self.btn_download.pack()
        
        # 日志框
        log_frame = tk.LabelFrame(main_frame, text='处理日志', 
                                 bg='white', fg='#495057',
                                 font=('Arial', 12, 'bold'))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                 wrap=tk.WORD,
                                                 font=('Consolas', 12),
                                                 bg='white', fg='#495057',
                                                 relief=tk.FLAT)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择要修复的ZIP或RWMod文件",
            filetypes=[("ZIP and RWMod Files", "*.zip *.rwmod"), ("ZIP Files", "*.zip"), ("RWMod Files", "*.rwmod"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_label.config(text=file_path)
            self.log_text.insert(tk.END, f"✅ 已选择文件: {os.path.basename(file_path)}\n")
            self.btn_start.config(state=tk.NORMAL)
            self.btn_download.config(state=tk.DISABLED)  # 新选择文件时禁用下载

    def start_processing(self):
        file_path = self.file_label.cget("text")
        if not file_path or file_path == "未选择文件":
            self.log_text.insert(tk.END, "❌ 请先选择一个ZIP或RWMOD文件！\n")
            return

        if not os.path.exists(file_path):
            self.log_text.insert(tk.END, "❌ 文件路径无效，文件不存在！\n")
            return

        self.btn_start.config(state=tk.DISABLED)
        self.log_text.insert(tk.END, "🚀 开始处理...\n")
        self.log_text.insert(tk.END, "-" * 50 + "\n")

        # 创建并启动工作线程
        def log_callback(msg):
            self.log_text.insert(tk.END, msg + "\n")
            self.log_text.see(tk.END)
            
        def finished_callback(final_zip_path):
            self.final_zip_path = final_zip_path
            self.btn_start.config(state=tk.NORMAL)
            if final_zip_path and os.path.exists(final_zip_path):
                self.btn_download.config(state=tk.NORMAL)
            else:
                self.btn_download.config(state=tk.DISABLED)
                
        self.worker = WorkerThread(file_path, log_callback, finished_callback)
        self.worker.start()

    def download_file(self):
        if self.final_zip_path and os.path.exists(self.final_zip_path):
            # 打开文件保存对话框，让用户选择下载位置
            save_path = filedialog.asksaveasfilename(
                title="保存修复后的文件",
                initialfile=os.path.basename(self.final_zip_path),
                defaultextension=".zip",
                filetypes=[("ZIP Files", "*.zip")]
            )
            if save_path:
                try:
                    import shutil
                    shutil.copy2(self.final_zip_path, save_path)
                    self.log_text.insert(tk.END, f"✅ 文件已成功保存到: {save_path}\n")
                except Exception as e:
                    self.log_text.insert(tk.END, f"❌ 保存文件时出错: {str(e)}\n")
        else:
            self.log_text.insert(tk.END, "❌ 文件不存在，无法下载。\n")

    def show(self):
        self.root.mainloop()


if __name__ == '__main__':
    window = ModernGUI()
    window.show()