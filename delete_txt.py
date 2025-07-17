#!/usr/bin/env python3
"""
删除指定目录下所有.txt文件的工具

用法:
  python delete_txt.py <目录路径>

功能:
  - 递归删除指定目录及其子目录中的所有.txt文件
  - 提供详细的删除报告
  - 安全的错误处理
"""

import os
import sys

def delete_txt_files(directory):
    """
    递归删除目录中所有.txt文件
    
    参数:
        directory (str): 要扫描的目录路径
        
    返回:
        list: 成功删除的文件路径列表
    """
    deleted_files = []
    
    # 遍历目录树
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查.txt扩展名
            if file.lower().endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    # 删除文件
                    os.remove(file_path)
                    deleted_files.append(file_path)
                    print(f"已删除: {file_path}")
                except PermissionError:
                    print(f"权限不足，无法删除: {file_path}")
                except Exception as e:
                    print(f"删除 {file_path} 时出错: {str(e)}")
    
    return deleted_files

def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("错误: 需要指定目标目录")
        print(f"用法: {sys.argv[0]} <目录路径>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    
    # 验证目录是否存在
    if not os.path.isdir(target_dir):
        print(f"错误: 目录不存在 - {target_dir}")
        sys.exit(1)
    
    print(f"\n正在扫描目录: {target_dir}")
    print("开始删除.txt文件...\n")
    
    # 执行删除操作
    deleted_files = delete_txt_files(target_dir)
    
    # 输出结果报告
    print("\n" + "="*50)
    print(f"删除完成! 共删除 {len(deleted_files)} 个.txt文件")
    
    if deleted_files:
        print("\n删除的文件列表:")
        for i, file_path in enumerate(deleted_files, 1):
            print(f"{i}. {file_path}")
    
    print("\n操作完成!")

if __name__ == "__main__":
    main()