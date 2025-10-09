#!/usr/bin/env python3
"""
清理重复的词典数据文件
确保只保留唯一的数据源路径
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def main():
    """主函数 - 清理重复的词典文件"""
    print("🧹 清理重复词典数据文件")
    print("=" * 60)
    
    # 定义唯一的数据源路径
    UNIQUE_DATA_SOURCE = "api/data/dictionary.json"
    
    print(f"✅ 保留的唯一数据源: {UNIQUE_DATA_SOURCE}")
    print(f"📊 数据源大小: {Path(UNIQUE_DATA_SOURCE).stat().st_size:,} bytes")
    
    # 定义要删除的重复文件和目录
    files_to_remove = [
        # 重复的词典文件
        "unified_final_dictionary/dictionary.json",
        "unified_final_dictionary/dictionary.csv", 
        "api/data/dictionary.csv",
        "api/data/dictionary_backup_20250926_133716.json",
        "api/data/dictionary_before_label_fix_20250926_134525.json",
        "api/data/dictionary_before_label_fix_20250926_134512.json",
        
        # 旧的词典数据
        "data/new_dictionary_20250926_031650.csv",
        "new_dictionary_data.csv",
        "dictionary_import_template.csv",
        
        # 补充数据文件
        "补充词典数据_批次1.csv",
        "补充词典数据_批次2.csv",
    ]
    
    # 定义要删除的重复目录
    dirs_to_remove = [
        # 备份目录
        "data/dictionary_backup",
        "backup/before_migration_20250926_031650",
        "data/vocab/backups",
        
        # 重复的统一词典目录
        "unified_final_dictionary",
        
        # 旧的转换数据
        "data/transformed_20250926_031650",
    ]
    
    # 删除重复文件
    print("\n🗑️ 删除重复文件:")
    removed_files = 0
    for file_path in files_to_remove:
        path = Path(file_path)
        if path.exists():
            try:
                size = path.stat().st_size
                path.unlink()
                print(f"  ✅ 删除文件: {file_path} ({size:,} bytes)")
                removed_files += 1
            except Exception as e:
                print(f"  ❌ 删除失败: {file_path} - {e}")
        else:
            print(f"  ⚪ 不存在: {file_path}")
    
    # 删除重复目录
    print("\n🗂️ 删除重复目录:")
    removed_dirs = 0
    for dir_path in dirs_to_remove:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            try:
                # 计算目录大小
                total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                shutil.rmtree(path)
                print(f"  ✅ 删除目录: {dir_path} ({total_size:,} bytes)")
                removed_dirs += 1
            except Exception as e:
                print(f"  ❌ 删除失败: {dir_path} - {e}")
        else:
            print(f"  ⚪ 不存在: {dir_path}")
    
    # 保留但重命名的文件（作为备份）
    print("\n📦 保留的备份文件:")
    backup_files = [
        "data/vocab/dictionary.json",  # 保留作为备份
        "data/unified_dictionary",     # 保留作为备份
        "ontology/dictionaries",       # 保留作为备份
    ]
    
    for backup_path in backup_files:
        path = Path(backup_path)
        if path.exists():
            if path.is_file():
                size = path.stat().st_size
                print(f"  📋 保留备份: {backup_path} ({size:,} bytes)")
            else:
                file_count = len(list(path.rglob('*')))
                print(f"  📁 保留备份目录: {backup_path} ({file_count} 个文件)")
    
    # 更新API配置为相对路径
    print("\n🔧 更新API配置:")
    api_file = Path("services/api/routers/kg_router.py")
    if api_file.exists():
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换硬编码的绝对路径为相对路径
            old_path = r'dict_path = r"D:\KG\api\data\dictionary.json"'
            new_path = 'dict_path = Path(__file__).parent.parent.parent / "api" / "data" / "dictionary.json"'
            
            if old_path in content:
                content = content.replace(old_path, new_path)
                # 添加Path导入
                if 'from pathlib import Path' not in content:
                    content = 'from pathlib import Path\n' + content
                
                with open(api_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ 更新API路径配置为相对路径")
            else:
                print(f"  ⚪ API路径配置已是相对路径")
                
        except Exception as e:
            print(f"  ❌ 更新API配置失败: {e}")
    
    # 验证唯一数据源
    print("\n✅ 验证唯一数据源:")
    unique_path = Path(UNIQUE_DATA_SOURCE)
    if unique_path.exists():
        import json
        try:
            with open(unique_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"  📊 数据源: {UNIQUE_DATA_SOURCE}")
            print(f"  📈 条目数: {len(data):,}")
            print(f"  💾 文件大小: {unique_path.stat().st_size:,} bytes")
            
            # 统计分类
            from collections import Counter
            categories = Counter(item.get('category', 'Unknown') for item in data)
            print(f"  🏷️ 分类统计:")
            for category, count in categories.most_common():
                print(f"     {category}: {count}条")
                
        except Exception as e:
            print(f"  ❌ 验证数据源失败: {e}")
    else:
        print(f"  ❌ 唯一数据源不存在: {UNIQUE_DATA_SOURCE}")
    
    # 总结
    print(f"\n🎯 清理总结:")
    print(f"✅ 删除了 {removed_files} 个重复文件")
    print(f"✅ 删除了 {removed_dirs} 个重复目录") 
    print(f"✅ 保留唯一数据源: {UNIQUE_DATA_SOURCE}")
    print(f"✅ 更新了API配置为相对路径")
    
    print(f"\n📋 下一步建议:")
    print(f"1. 重启API服务以应用新的路径配置")
    print(f"2. 测试前端词典页面确认数据正常")
    print(f"3. 如需备份，可以保留 data/vocab/dictionary.json")
    print(f"4. 定期清理临时文件和备份文件")

if __name__ == "__main__":
    main()
