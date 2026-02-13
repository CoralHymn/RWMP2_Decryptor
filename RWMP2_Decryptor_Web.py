import os
import zipfile
from pathlib import Path
from pywebio import start_server
from pywebio.input import file_upload, actions
from pywebio.output import put_text, put_markdown, put_file, clear, put_loading, use_scope
from pywebio.session import hold
# ============= 新增的导入 =============
import threading  # 修复bug 2
import time

# ============= 导入RWMP2_Decryptor模块 =============
from RWMP2_Decryptor import reverse_replace_in_zip, AdvancedZipRepair, process_rwmod_file

def main():
    print("琴海奶油版权所属，遵循MIT开源协议")
    print("目前版本为 Alpha2.2.0")
    print("查看教程前往官网：https://coralhymn.com")
    zip_file_path = input("请输入要修复的ZIP文件路径: ").strip().strip('"')
    
    if not os.path.exists(zip_file_path):
        print("文件不存在!")
        return
    
    if not zip_file_path.lower().endswith('.zip'):
        print("请提供ZIP文件!")
        return
    
    # 第一步：执行逆向替换预处理
    print("第一步：执行逆向替换预处理...")
    processed_data = reverse_replace_in_zip(zip_file_path)
    
    # 第二步：使用处理后的数据进行修复
    print("\n第二步：开始修复ZIP文件...")
    repair_tool = AdvancedZipRepair(zip_file_path, processed_data)
    
    # 开始修复
    repair_tool.repair_zip()

def web_main():
    """铁锈模组加密器网页版"""
    put_markdown("# 🛠️ RWMP2_Decryptor_Web ")

    # 1. 选择文件
    put_markdown("### 📁 1. 请选择要修复的ZIP文件\n官网:https://coralhymn.com \nGithub:https://github.com/CoralHymn/RWMP2_Decryptor")
    uploaded_file = file_upload(
        label="点击上传或拖拽文件",
        accept='.zip,.rwmod',
        placeholder='请选择一个 .zip 或 .rwmod 文件...'
    )

    if not uploaded_file:
        put_text("❌ 未选择文件，请重新加载。")
    #    return

    # 创建临时工作目录
    temp_dir = Path("temp_web_session")
    temp_dir.mkdir(exist_ok=True)

    # 保存上传的文件
    original_file_path = temp_dir / uploaded_file['filename']
    with open(original_file_path, 'wb') as f:
        f.write(uploaded_file['content'])

    # 检查并处理.rwmod文件
    processed_file_path = process_rwmod_file(str(original_file_path))
    if processed_file_path is None:
        put_text("❌ 文件处理失败!")
        return

    put_text(f"✅ 文件 '{uploaded_file['filename']}' 上传成功！")

    # 2. 开始处理按钮
    put_markdown("### ⚙️ 2. 开始处理")
    confirm = actions('准备就绪，开始处理吗？', [
        {'label': '开始修复', 'value': 'start', 'color': 'primary'},
        {'label': '取消', 'value': 'cancel', 'color': 'secondary'}
    ])

    if confirm != 'start':
        put_text("❌ 操作已取消。")
        return

    # 显示加载动画
    with use_scope('loading', clear=True):
        put_loading(color='primary')
        put_text("正在处理文件，请稍候...")

    # 执行处理流程
    try:
        # 第一步：执行逆向替换预处理
        processed_data = reverse_replace_in_zip(processed_file_path)

        # 第二步：使用处理后的数据进行修复
        repair_tool = AdvancedZipRepair(processed_file_path, processed_data)
        
        # 模仿repair_zip的核心逻辑，但跳过最后的打包和清理
        if not repair_tool.save_temp_file():
            raise Exception("创建临时文件失败")

        os.makedirs(repair_tool.repaired_dir, exist_ok=True)

        print("正在扫描文件头...")
        headers = repair_tool.find_local_headers()
        if not headers:
            raise Exception("未找到有效的文件头")

        success_count = 0
        for i, header in enumerate(headers):
            if i % 50 == 0:
                print(f"处理进度: {i+1}/{len(headers)}")
            filename = header['filename']
            file_data = repair_tool.extract_file_data(header)
            if file_data is not None and len(file_data) > 0:
                if repair_tool.save_file(filename, file_data):
                    success_count += 1

        # 执行批量重命名
        repair_tool.batch_rename_files()

        # 清理临时处理文件（如_temp_processed.zip）
        repair_tool.cleanup_temp_file()

        if success_count == 0:
            raise Exception("没有成功提取任何文件")

        # 由web_main函数手动打包_repaired目录
        repaired_dir_path = Path(repair_tool.repaired_dir)
        final_zip_filename = Path(processed_file_path).stem + "_最终修复.zip"  # 这是用户下载时看到的文件名
        final_zip_path = temp_dir / final_zip_filename

        with zipfile.ZipFile(final_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(repaired_dir_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(repaired_dir_path)
                    zipf.write(file_path, arcname)

        # ========== 修复点1：清理_repaired文件夹 ==========
        import shutil
        if repaired_dir_path.exists():
            shutil.rmtree(repaired_dir_path)
            print("已清理临时修复目录")

        # 处理成功
        clear('loading')
        put_markdown("### 🎉 3. 处理完成！")
        put_text(f"成功修复文件: {final_zip_filename}")
        put_text(f"共提取了 {success_count} 个文件。")
        
        # ========== 修复点：确保下载文件名正确 ==========
        with open(final_zip_path, 'rb') as f:
            file_content = f.read()
        
        # 关键：打印出我们打算用作文件名的变量，用于调试
        print(f"DEBUG: 最终的下载文件名是 -> {final_zip_filename}")
        
        # put_file(label, content, filename)
        # label: 显示在页面上的文字
        # filename: 用户下载时保存的文件名
        put_file(
            name=final_zip_filename,          # 第一个参数是下载的文件名，你可以加上自己的署名
            content=file_content,             # 第二个参数是文件内容
            label='📥 点击下载修复后的文件'    # 第三个参数是显示的文字
)

        # ========== 修复点：使用Timer延迟清理原始上传的zip文件 ==========
        def cleanup_all_temp_files():
            """在30秒后清理本次操作产生的所有临时文件"""
            #为保证服务器无垃圾残留，如果你是个人电脑可以删掉这一部分
            try:
                # 等待30秒
                time.sleep(30)
                
                # 清理1: 原始上传的文件
                if original_file_path.exists():
                    os.remove(original_file_path)
                    print(f"✅ 已清理临时上传文件: {original_file_path}")
                else:
                    print(f"⚠️ 临时上传文件已不存在: {original_file_path}")

                # 清理2: 我们生成的“最终修复.zip”文件
                if final_zip_path.exists():
                    os.remove(final_zip_path)
                    print(f"✅ 已清理生成的最终修复文件: {final_zip_path}")
                else:
                    print(f"⚠️ 最终修复文件已不存在: {final_zip_path}")

                # 如果处理的是.rwmod文件，还要清理重命名后的.zip文件
                if processed_file_path != str(original_file_path) and os.path.exists(processed_file_path):
                    os.remove(processed_file_path)
                    print(f"✅ 已清理重命名后的文件: {processed_file_path}")

            except Exception as e:
                print(f"❌ 延迟清理文件时出错: {e}")

        # 使用 threading.Timer 在30秒后执行清理
        cleanup_timer = threading.Timer(30.0, cleanup_all_temp_files)
        cleanup_timer.daemon = True
        cleanup_timer.start()
        
    except Exception as e:
        clear('loading')
        put_text(f"❌ 处理过程中发生错误: {str(e)}")
        import traceback
        put_text("详细错误信息:")
        put_text(traceback.format_exc())

if __name__ == '__main__':
    print("正在启动Web服务器... 访问 http://localhost:8085")
    #在个人电脑上会随机放一个端口，你如果不想要自动启动把下面的"web_main,"删掉
    #8085端口是为服务器服务的，如果你的服务器端口想换成其他的直接换下方的port数值
    start_server(web_main, port=8085, debug=True, host='localhost', auto_open_webbrowser=True)
