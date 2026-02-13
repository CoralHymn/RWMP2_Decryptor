import os
import struct
import zlib
import zipfile
import sys
from pathlib import Path
import hashlib
from collections import defaultdict


def reverse_replace_in_zip(zip_file_path):
    """执行解密替换的预处理功能，返回处理后的数据"""
    # 替换反斜杠（用于执行字节序列的替换操作）
    # 如果你发现有其他文件变成了文件夹，可以自行在下方加上（别忘了后面也有代码）
    # 用16进制编码加上，如果不懂可以复制下面一段问ai
    # 例如
    #    2E 74 78 74 2F（ASCII: ".txt/"）→ 替换为 2E 74 78 74 31（ASCII: ".txt1"）

    replacements = {
        bytes.fromhex('2E 74 78 74 2F'): bytes.fromhex('2E 74 78 74 31'),
        bytes.fromhex('2E 69 6E 69 2F'): bytes.fromhex('2E 69 6E 69 31'),
        bytes.fromhex('2E 70 6E 67 2F'): bytes.fromhex('2E 70 6E 67 31')
    }
    
    try:
        # 读取原始文件内容
        with open(zip_file_path, 'rb') as f:
            data = f.read()
        
        # 执行替换
        modified = False
        for old, new in replacements.items():
            if old in data:
                data = data.replace(old, new)
                modified = True
        
        if not modified:
            print("没有找到需要逆向替换的字节序列。")
            return None  # 返回None表示没有修改
        
        print("逆向替换完成")
        return data  # 返回处理后的数据
    
    except Exception as e:
        print(f"逆向替换发生错误: {e}")
        return None  # 出错时返回None

class AdvancedZipRepair:
    def __init__(self, zip_path, processed_data=None):
        self.original_zip_path = zip_path  # 保存原始文件路径
        self.processed_data = processed_data  # 处理后的数据
        if processed_data is not None:
            # 如果有处理后的数据，创建临时文件路径
            self.zip_path = zip_path.replace('.zip', '_temp_processed.zip')
        else:
            self.zip_path = zip_path
        self.repaired_dir = Path(zip_path).stem + "_repaired"
        self.extracted_files = {}  # 记录已提取的文件
        self.duplicate_count = 0   # 重复文件计数
        
    def save_temp_file(self):
        """保存处理后的数据到临时文件"""
        if self.processed_data is not None:
            try:
                with open(self.zip_path, 'wb') as f:
                    f.write(self.processed_data)
                print(f"已创建临时处理文件: {self.zip_path}")
            except Exception as e:
                print(f"创建临时文件失败: {e}")
                return False
        return True
    
    def cleanup_temp_file(self):
        """清理临时文件"""
        if self.processed_data is not None and os.path.exists(self.zip_path):
            try:
                os.remove(self.zip_path)
                print("已清理临时文件")
            except Exception as e:
                print(f"清理临时文件失败: {e}")
        
    def find_local_headers(self):
        """扫描ZIP文件，查找所有有效的Local File Header"""
        headers = []
        try:
            # 根据是否有处理后的数据选择读取方式
            if self.processed_data is not None:
                data = self.processed_data
            else:
                with open(self.zip_path, 'rb') as f:
                    data = f.read()
                
            offset = 0
            file_count = 0
            while offset < len(data) - 30:
                # 查找ZIP Local File Header签名
                if data[offset:offset+4] == b'PK\x03\x04':
                    try:
                        header_info = self.parse_local_header(data, offset)
                        if header_info:
                            headers.append(header_info)
                            file_count += 1
                            if file_count % 100 == 0:
                                print(f"已扫描 {file_count} 个文件...")
                        # 跳到下一个可能的位置
                        if header_info and header_info.get('compressed_size', 0) > 0:
                            offset += 30 + len(header_info.get('filename', '')) + \
                                     header_info.get('extra_length', 0) + \
                                     header_info.get('compressed_size', 0)
                        else:
                            offset += 1
                    except Exception as e:
                        offset += 1
                else:
                    offset += 1
                    
        except Exception as e:
            print(f"读取文件时出错: {e}")
            
        return headers
    
    def parse_local_header(self, data, offset):
        """解析Local File Header"""
        try:
            # 检查是否有足够的数据
            if offset + 30 > len(data):
                return None
                
            # 读取基础信息
            signature = struct.unpack('<I', data[offset:offset+4])[0]
            version = struct.unpack('<H', data[offset+4:offset+6])[0]
            flags = struct.unpack('<H', data[offset+6:offset+8])[0]
            compression = struct.unpack('<H', data[offset+8:offset+10])[0]
            mod_time = struct.unpack('<H', data[offset+10:offset+12])[0]
            mod_date = struct.unpack('<H', data[offset+12:offset+14])[0]
            crc32 = struct.unpack('<I', data[offset+14:offset+18])[0]
            compressed_size = struct.unpack('<I', data[offset+18:offset+22])[0]
            uncompressed_size = struct.unpack('<I', data[offset+22:offset+26])[0]
            filename_length = struct.unpack('<H', data[offset+26:offset+28])[0]
            extra_length = struct.unpack('<H', data[offset+28:offset+30])[0]
            
            # 检查长度是否合理
            if filename_length > 1000 or compressed_size > len(data):
                return None
                
            # 读取文件名
            filename_start = offset + 30
            filename_end = filename_start + filename_length
            
            if filename_end > len(data):
                return None
                
            try:
                filename = data[filename_start:filename_end].decode('utf-8')
            except:
                try:
                    filename = data[filename_start:filename_end].decode('gbk')
                except:
                    filename = data[filename_start:filename_end].decode('utf-8', errors='ignore')
            
            # 清理文件名
            filename = self.clean_filename(filename)
            
            # 计算数据位置
            data_start = filename_end + extra_length
            data_end = data_start + compressed_size
            
            return {
                'offset': offset,
                'filename': filename,
                'compressed_size': compressed_size,
                'uncompressed_size': uncompressed_size,
                'compression_method': compression,
                'data_start': data_start,
                'data_end': data_end,
                'crc32': crc32,
                'extra_length': extra_length
            }
        except Exception as e:
            return None
    
    def clean_filename(self, filename):
        """清理文件名，移除非法字符"""
        illegal_chars = '<>:"|?*'
        for char in illegal_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def generate_unique_filename(self, original_filename):
        """生成唯一文件名，避免覆盖"""
        base_name = original_filename
        counter = 1
        
        # 检查是否已存在
        while base_name in self.extracted_files:
            # 分离文件名和扩展名
            path_obj = Path(original_filename)
            if path_obj.suffix:
                new_name = f"{path_obj.stem}_{counter}{path_obj.suffix}"
                base_name = str(path_obj.parent / new_name) if path_obj.parent != Path('.') else new_name
            else:
                base_name = f"{original_filename}_{counter}"
            counter += 1
            
        return base_name
    
    def extract_file_data(self, header_info):
        """提取单个文件的数据"""
        try:
            # 根据是否有处理后的数据选择读取方式
            if self.processed_data is not None:
                # 直接从内存数据中提取
                data_start = header_info['data_start']
                data_end = min(header_info['data_end'], len(self.processed_data))
                compressed_data = self.processed_data[data_start:data_end]
            else:
                with open(self.zip_path, 'rb') as f:
                    # 检查边界
                    file_size = os.path.getsize(self.zip_path)
                    if header_info['data_start'] >= file_size:
                        return None
                        
                    f.seek(header_info['data_start'])
                    # 只读取可用的数据
                    available_size = file_size - header_info['data_start']
                    read_size = min(header_info['compressed_size'], available_size)
                    compressed_data = f.read(read_size)
                
            # 根据压缩方法解压
            if header_info['compression_method'] == 0:  # 存储（无压缩）
                return compressed_data
            elif header_info['compression_method'] == 8:  # Deflate压缩
                try:
                    return zlib.decompress(compressed_data, -zlib.MAX_WBITS)
                except Exception:
                    # 尝试忽略错误的解压
                    try:
                        decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
                        result = decompressor.decompress(compressed_data)
                        return result
                    except Exception:
                        print(f"  警告: {header_info['filename']} 解压失败")
                        return compressed_data  # 返回原始数据
            else:
                print(f"  警告: 不支持的压缩方法 {header_info['compression_method']}")
                return compressed_data  # 返回原始数据
        except Exception as e:
            print(f"  错误: 提取数据失败 - {e}")
            return None
    
    def save_file(self, filename, file_data):
        """保存文件，处理重复文件名"""
        # 生成唯一文件名
        unique_filename = self.generate_unique_filename(filename)
        
        # 创建完整路径
        full_path = Path(self.repaired_dir) / unique_filename
        
        # 确保目录存在
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文件
        try:
            with open(full_path, 'wb') as f:
                f.write(file_data)
            
            # 记录已提取的文件
            self.extracted_files[unique_filename] = len(file_data)
            
            if unique_filename != filename:
                print(f"  文件名冲突，保存为: {unique_filename}")
            
            return True
        except Exception as e:
            print(f"  保存文件失败: {e}")
            return False
    
    def create_repaired_zip(self):
        """将修复的文件打包成ZIP文件"""
        repaired_zip_path = Path(self.original_zip_path).stem + "_最终修复.zip"  # 使用原始文件名
        print(f"\n正在创建修复后的ZIP文件: {repaired_zip_path}")
        
        try:
            with zipfile.ZipFile(repaired_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                file_count = 0
                for root, dirs, files in os.walk(self.repaired_dir):
                    for file in files:
                        file_path = Path(root) / file
                        # 计算相对路径
                        arcname = file_path.relative_to(self.repaired_dir)
                        zipf.write(file_path, arcname)
                        file_count += 1
                        if file_count % 50 == 0:
                            print(f"已添加 {file_count} 个文件到ZIP...")
                
            print(f"✓ 成功创建修复ZIP文件: {repaired_zip_path}")
            print(f"包含文件数: {file_count}")
            return repaired_zip_path
        except Exception as e:
            print(f"✗ 创建ZIP文件失败: {e}")
            return None
    
    def batch_rename_files(self):
        """批量重命名文件，修复扩展名"""
        print("\n开始批量重命名文件...")
        
        # 定义需要修复的扩展名映射
        extension_mapping = {
            '.ini1': '.ini',
            '.txt1': '.txt',
            '.png1': '.png',
            '.jpg1': '.jpg',
            '.jpeg1': '.jpeg',
            '.bmp1': '.bmp',
            '.gif1': '.gif',
            '.pdf1': '.pdf',
            '.doc1': '.doc',
            '.docx1': '.docx',
            '.xls1': '.xls',
            '.xlsx1': '.xlsx'
        }
        
        renamed_count = 0
        error_count = 0
        
        for root, dirs, files in os.walk(self.repaired_dir):
            for file in files:
                file_path = Path(root) / file
                suffix = file_path.suffix.lower()
                
                # 检查是否需要重命名
                if suffix in extension_mapping:
                    new_suffix = extension_mapping[suffix]
                    new_name = file_path.stem + new_suffix
                    new_path = file_path.parent / new_name
                    
                    # 检查新文件名是否已存在
                    if new_path.exists():
                        # 如果存在，添加数字后缀
                        counter = 1
                        while (file_path.parent / f"{file_path.stem}_{counter}{new_suffix}").exists():
                            counter += 1
                        new_path = file_path.parent / f"{file_path.stem}_{counter}{new_suffix}"
                    
                    try:
                        file_path.rename(new_path)
                        print(f"  重命名: {file} -> {new_path.name}")
                        renamed_count += 1
                    except Exception as e:
                        print(f"  重命名失败 {file}: {e}")
                        error_count += 1
        
        print(f"批量重命名完成!")
        print(f"成功重命名: {renamed_count} 个文件")
        if error_count > 0:
            print(f"重命名失败: {error_count} 个文件")
        
        return renamed_count
    
    def repair_zip(self):
        """主修复函数"""
        # 如果有处理后的数据，先保存临时文件
        if not self.save_temp_file():
            return False
            
        print(f"开始修复ZIP文件: {self.original_zip_path}")
        if self.processed_data is not None:
            print("使用预处理后的数据进行修复")
            print(f"处理后数据大小: {len(self.processed_data) / 1024 / 1024:.2f} MB")
        else:
            print(f"文件大小: {os.path.getsize(self.zip_path) / 1024 / 1024:.2f} MB")
        
        # 创建修复目录
        os.makedirs(self.repaired_dir, exist_ok=True)
        
        # 查找所有文件头
        print("正在扫描文件头...")
        headers = self.find_local_headers()
        
        if not headers:
            print("未找到有效的文件头")
            self.cleanup_temp_file()
            return False
            
        print(f"总共找到 {len(headers)} 个文件")
        
        # 尝试提取每个文件
        success_count = 0
        failed_count = 0
        
        for i, header in enumerate(headers):
            if i % 50 == 0:
                print(f"处理进度: {i+1}/{len(headers)}")
            
            filename = header['filename']
            print(f"\n处理文件 {i+1}/{len(headers)}: {filename}")
            print(f"  压缩大小: {header['compressed_size']} bytes")
            print(f"  原始大小: {header['uncompressed_size']} bytes")
            
            # 提取数据
            file_data = self.extract_file_data(header)
            if file_data is not None and len(file_data) > 0:
                # 保存文件
                if self.save_file(filename, file_data):
                    print(f"  ✓ 成功提取: {filename} ({len(file_data)} bytes)")
                    success_count += 1
                else:
                    print(f"  ✗ 保存失败: {filename}")
                    failed_count += 1
            else:
                print(f"  ✗ 提取失败: {filename}")
                failed_count += 1
        
        # 输出统计信息
        print(f"\n" + "="*50)
        print(f"修复完成!")
        print(f"扫描文件数: {len(headers)}")
        print(f"成功提取: {success_count}")
        print(f"提取失败: {failed_count}")
        print(f"重复文件处理: {self.duplicate_count}")
        print(f"实际文件数: {len(self.extracted_files)}")
        print(f"修复文件保存在: {self.repaired_dir}")
        
        # 显示文件结构
        self.show_file_structure()
        
        # 新增功能：批量重命名
        renamed_count = self.batch_rename_files()
        
        # 新增功能：创建修复后的ZIP文件
        zip_path = self.create_repaired_zip()
        
        # 清理临时文件
        self.cleanup_temp_file()
        
        # 清理修复目录
        self.cleanup_repair_directory()
        
        if zip_path:
            print(f"\n🎉 修复流程完成!")
            print(f"   - 提取文件: {success_count} 个")
            print(f"   - 重命名文件: {renamed_count} 个")
            print(f"   - 最终ZIP文件: {zip_path}")
        
        return success_count > 0
    
    def cleanup_repair_directory(self):
        """清理修复目录"""
        try:
            import shutil
            if os.path.exists(self.repaired_dir):
                shutil.rmtree(self.repaired_dir)
                print("已清理临时修复目录")
        except Exception as e:
            print(f"清理修复目录失败: {e}")
    
    def show_file_structure(self):
        """显示提取的文件结构"""
        print(f"\n文件结构预览:")
        print("-" * 30)
        
        # 统计文件类型
        extensions = defaultdict(int)
        total_size = 0
        
        for filename, size in self.extracted_files.items():
            ext = Path(filename).suffix.lower()
            extensions[ext] += 1
            total_size += size
            
        print(f"总文件大小: {total_size / 1024 / 1024:.2f} MB")
        print("文件类型统计:")
        for ext, count in sorted(extensions.items()):
            print(f"  {ext or '(无扩展名)'}: {count} 个文件")

def process_rwmod_file(file_path):
    """处理.rwmod文件，将其重命名为.zip后缀"""
    if file_path.lower().endswith('.rwmod'):
        # 创建新的文件路径，将.rwmod改为.zip
        new_file_path = file_path[:-6] + '.zip'
        
        # 检查目标文件是否已存在
        if os.path.exists(new_file_path):
            print(f"警告: 目标文件 {new_file_path} 已存在，将覆盖原文件")
            
        try:
            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f"已将 {file_path} 重命名为 {new_file_path}")
            return new_file_path
        except Exception as e:
            print(f"重命名文件失败: {e}")
            return None
    else:
        # 如果不是.rwmod文件，直接返回原路径
        return file_path

def main():
    print("琴海奶油版权所属，遵循MIT开源协议")
    print("目前版本为 Alpha2.1.0")
    print("查看教程前往官网：https://coralhymn.com")
    file_path = input("请输入要修复的文件路径: ").strip().strip('"')
    
    if not os.path.exists(zip_file_path):
        print("文件不存在!")
        return
    
    # 检查并处理.rwmod文件
    processed_file_path = process_rwmod_file(file_path)
    if processed_file_path is None:
        print("文件处理失败!")
        return
    
    # 检查是否为ZIP文件（包括刚重命名的文件）
    if not processed_file_path.lower().endswith('.zip'):
        print("请提供ZIP文件或.rwmod文件!")
        return
    
    # 第一步：执行逆向替换预处理
    print("第一步：执行逆向替换预处理...")
    processed_data = reverse_replace_in_zip(processed_file_path)
    
    # 第二步：使用处理后的数据进行修复
    print("\n第二步：开始修复ZIP文件...")
    repair_tool = AdvancedZipRepair(processed_file_path, processed_data)
    
    # 开始修复
    repair_tool.repair_zip()

if __name__ == "__main__":
    main()
