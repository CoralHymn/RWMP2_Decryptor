import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QTextEdit, QLabel,
                             QFrame, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor


from RWMP2_Decryptor import reverse_replace_in_zip, AdvancedZipRepair

class WorkerThread(QThread):
    """一个在后台运行原修复脚本的线程"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str)  # 发出最终ZIP文件的路径

    def __init__(self, zip_path):
        super().__init__()
        self.zip_path = zip_path

    def run(self):
        try:
            self.log_signal.emit("第一步：执行逆向替换预处理...")
            processed_data = reverse_replace_in_zip(self.zip_path)

            self.log_signal.emit("\n第二步：开始修复ZIP文件...")
            repair_tool = AdvancedZipRepair(self.zip_path, processed_data)
            # 重定向原脚本的print输出到GUI
            import builtins
            original_print = builtins.print

            def gui_print(*args, **kwargs):
                msg = ' '.join(map(str, args))
                self.log_signal.emit(msg)

            builtins.print = gui_print

            success = repair_tool.repair_zip()

            # 恢复print函数
            builtins.print = original_print

            if success:
                # 尝试找到生成的最终ZIP文件
                stem = os.path.splitext(os.path.basename(self.zip_path))[0]
                final_zip = f"{stem}_最终修复.zip"
                if os.path.exists(final_zip):
                    self.finished_signal.emit(final_zip)
                    self.log_signal.emit(f"\n🎉 处理成功！修复后的文件已生成：{final_zip}")
                else:
                    self.finished_signal.emit("")
                    self.log_signal.emit("\n处理成功，但未找到最终ZIP文件。")
            else:
                self.finished_signal.emit("")
                self.log_signal.emit("\n❌ 处理失败。")

        except Exception as e:
            import traceback
            self.log_signal.emit(f"\n❌ 处理过程中发生严重错误：{str(e)}")
            self.log_signal.emit(traceback.format_exc())
            self.finished_signal.emit("")


class ModernGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.final_zip_path = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle('RWMP2_Decryptor2.0.2')
        self.setMinimumSize(600, 500)

        # 设置整体样式
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QPushButton {
                background-color: #4361ee;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #3a56d4;
            }
            QPushButton:disabled {
                background-color: #adb5bd;
            }
            QPushButton#download_btn {
                background-color: #2a9d8f;
            }
            QPushButton#download_btn:hover {
                background-color: #238b7d;
            }
            QPushButton#download_btn:disabled {
                background-color: #6c757d;
            }
            QLabel {
                color: #2b2d42;
                font-size: 14px;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 8px;
                padding: 10px;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 12px;
                color: #495057;
            }
        """)

        # 主布局
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title = QLabel('RWMP2 Decryptor GUI')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setStyleSheet("color: #2b2d42; margin-bottom: 10px;")
        layout.addWidget(title)

        subtitle = QLabel('开源的铁锈模组解密器\n官网:https://coralhymn.com \nGithub:https://github.com/CoralHymn/RWMP2_Decryptor')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #6c757d; font-size: 13px; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        # 文件选择区域
        file_layout = QHBoxLayout()
        self.file_label = QLabel('未选择文件')
        self.file_label.setWordWrap(True)
        self.file_label.setStyleSheet("background-color: white; border-radius: 8px; padding: 8px; color: #6c757d;")
        self.file_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        btn_select = QPushButton('选择ZIP文件')
        btn_select.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(btn_select)
        layout.addLayout(file_layout)

        # 开始按钮
        self.btn_start = QPushButton('开始处理')
        self.btn_start.clicked.connect(self.start_processing)
        self.btn_start.setMaximumWidth(200)
        self.btn_start.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.btn_start, alignment=Qt.AlignCenter)

        # 下载区域
        download_layout = QHBoxLayout()
        download_layout.addStretch(1)
        self.btn_download = QPushButton('下载处理结果')
        self.btn_download.setObjectName("download_btn")
        self.btn_download.clicked.connect(self.download_file)
        self.btn_download.setEnabled(False)
        self.btn_download.setMaximumWidth(200)
        self.btn_download.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        download_layout.addWidget(self.btn_download)
        download_layout.addStretch(1)
        layout.addLayout(download_layout)

        # 日志框 (放在一个滚动区域中)
        log_frame = QFrame()
        log_frame.setFrameShape(QFrame.StyledPanel)
        log_frame.setStyleSheet("background-color: white; border-radius: 8px;")

        log_layout = QVBoxLayout()
        log_layout.setContentsMargins(5, 5, 5, 5)
        log_title = QLabel('处理日志')
        log_title.setStyleSheet("color: #495057; font-weight: bold; padding: 5px;")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(log_title)
        log_layout.addWidget(self.log_text)
        log_frame.setLayout(log_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(log_frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        layout.addWidget(scroll_area, stretch=1)

        self.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择要修复的ZIP文件",
            "",
            "ZIP Files (*.zip);;All Files (*)",
            options=options
        )
        if file_path:
            self.file_label.setText(file_path)
            self.log_text.append(f"✅ 已选择文件: {os.path.basename(file_path)}")
            self.btn_start.setEnabled(True)
            self.btn_download.setEnabled(False)  # 新选择文件时禁用下载

    def start_processing(self):
        file_path = self.file_label.text()
        if not file_path or file_path == "未选择文件":
            self.log_text.append("❌ 请先选择一个ZIP文件！")
            return

        if not os.path.exists(file_path):
            self.log_text.append("❌ 文件路径无效，文件不存在！")
            return

        self.btn_start.setEnabled(False)
        self.log_text.append("🚀 开始处理...")
        self.log_text.append("-" * 50)

        # 创建并启动工作线程
        self.worker = WorkerThread(file_path)
        self.worker.log_signal.connect(self.log_text.append)
        self.worker.finished_signal.connect(self.on_processing_finished)
        self.worker.start()

    def on_processing_finished(self, final_zip_path):
        self.final_zip_path = final_zip_path
        self.btn_start.setEnabled(True)
        if final_zip_path and os.path.exists(final_zip_path):
            self.btn_download.setEnabled(True)
        else:
            self.btn_download.setEnabled(False)

    def download_file(self):
        if self.final_zip_path and os.path.exists(self.final_zip_path):
            # 打开文件保存对话框，让用户选择下载位置
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存修复后的文件",
                os.path.basename(self.final_zip_path),  # 默认文件名
                "ZIP Files (*.zip)"
            )
            if save_path:
                try:
                    import shutil
                    shutil.copy2(self.final_zip_path, save_path)
                    self.log_text.append(f"✅ 文件已成功保存到: {save_path}")
                except Exception as e:
                    self.log_text.append(f"❌ 保存文件时出错: {str(e)}")
        else:
            self.log_text.append("❌ 文件不存在，无法下载。")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ModernGUI()
    window.show()
    sys.exit(app.exec_())