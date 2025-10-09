#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行最终清理 - 删除已清空的文件和剩余的冗余文件
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def check_empty_files():
    """检查空文件或只有注释的文件"""
    print("🔍 检查空文件和无效文件...")
    
    empty_files = []
    root_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.py')]
    
    for file in root_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            # 检查是否为空文件或只有简单注释
            if not content or content == '#' or len(content.split('\n')) <= 2:
                empty_files.append(file)
                print(f"   📄 发现空文件: {file}")
        except Exception as e:
            print(f"   ⚠️ 无法读取文件 {file}: {e}")
    
    return empty_files

def identify_remaining_duplicates():
    """识别剩余的重复文件"""
    print("\n🔍 识别剩余的重复文件...")
    
    remaining_duplicates = []
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    # 按功能分组检查重复
    function_groups = {
        "数据导入脚本": [],
        "统计报告": [],
        "词典总结": [],
        "测试文件": [],
        "验证脚本": []
    }
    
    for file in root_files:
        file_lower = file.lower()
        
        # 数据导入相关
        if any(keyword in file for keyword in ['全部', '硬件模块', '数据导入', '批次']):
            function_groups["数据导入脚本"].append(file)
        
        # 统计报告
        elif any(keyword in file for keyword in ['统计报告', 'json']) and '硬件' in file:
            function_groups["统计报告"].append(file)
        
        # 词典总结
        elif any(keyword in file for keyword in ['词典', '总结', '扩展', '史诗']) and file.endswith('.md'):
            function_groups["词典总结"].append(file)
        
        # 测试文件
        elif file.startswith('test_') and file.endswith(('.py', '.html')):
            function_groups["测试文件"].append(file)
        
        # 验证脚本
        elif any(keyword in file for keyword in ['验证', '检查', '测试']) and file.endswith('.py'):
            function_groups["验证脚本"].append(file)
    
    # 显示重复组
    for group, files in function_groups.items():
        if len(files) > 3:  # 超过3个认为是重复
            print(f"   📂 {group} (重复{len(files)}个):")
            for file in files[:5]:  # 显示前5个
                print(f"      - {file}")
            remaining_duplicates.extend(files[3:])  # 保留前3个，其余标记为重复
    
    return remaining_duplicates

def execute_final_cleanup():
    """执行最终清理"""
    print("🧹 执行最终清理")
    print("=" * 60)
    
    # 创建最终备份
    backup_dir = f"final_cleanup_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    print(f"📦 创建最终备份: {backup_dir}")
    
    cleanup_count = 0
    
    # 1. 删除已清空的文件
    print(f"\n🗑️ 删除已清空的文件...")
    empty_files = check_empty_files()
    
    for file in empty_files:
        if os.path.exists(file):
            # 备份
            shutil.copy2(file, backup_dir)
            # 删除
            os.remove(file)
            print(f"   ✅ 删除空文件: {file}")
            cleanup_count += 1
    
    # 2. 删除明确的重复文件
    print(f"\n🗑️ 删除明确的重复文件...")
    
    duplicate_files = [
        # 重复的数据导入脚本（保留最新的）
        "全部12个硬件模块数据导入脚本.cypher",
        "全部16个硬件模块数据导入脚本.cypher", 
        "全部20个硬件模块数据导入脚本.cypher",
        "新增硬件模块数据导入脚本.cypher",
        "第三批硬件模块数据导入脚本.cypher",
        "第四批硬件模块数据导入脚本.cypher",
        "第五批硬件模块数据导入脚本.cypher",
        "硬件模块数据导入脚本.cypher",
        "更新图谱数据导入脚本.cypher",
        
        # 重复的统计报告（保留最新的）
        "全部12个硬件模块数据统计报告.json",
        "全部16个硬件模块数据统计报告.json",
        "全部20个硬件模块数据统计报告.json",
        "新增硬件模块数据统计报告.json",
        "第三批硬件模块数据统计报告.json",
        "第四批硬件模块数据统计报告.json",
        "第五批硬件模块数据统计报告.json",
        "硬件模块数据统计报告.json",
        "补充数据统计报告.json",
        
        # 重复的词典总结文档
        "词典图谱史诗级扩展完成总结.md",
        "词典图谱拓展完成总结.md",
        "词典图谱终极史诗级扩展完成总结.md",
        "词典图谱终极扩展完成总结.md",
        "词典图谱补充完善总结.md",
        "词典图谱超级史诗级扩展完成总结.md",
        "词典数据修复完成总结.md",
        "词典系统全面分析报告.md",
        "词典系统全面解析完成总结.md",
        "词典系统深度数据分析报告.md",
        
        # 重复的更新总结
        "图谱更新总结.json",
        "图谱更新成功总结.md",
        "图谱更新最终总结.md",
        
        # 重复的合并报告
        "完整补充数据合并报告.json",
        "最终完整补充数据合并报告.json",
        "终极完整补充数据合并报告.json",
        "终极完整补充数据合并报告_16模块版.json",
        "终极完整补充数据合并报告_20模块版.json",
        
        # 重复的导入脚本
        "完整词典补充数据导入脚本.cypher",
        "最终完整词典补充数据导入脚本.cypher",
        "终极完整词典补充数据导入脚本.cypher",
        "终极完整词典补充数据导入脚本_16模块版.cypher",
        "终极完整词典补充数据导入脚本_20模块版.cypher",
        
        # 重复的测试文件
        "test_display.xlsx",
        "test_excel_parsing.xlsx",
        "test_frontend.html",
        "test_system_management.html",
        
        # 重复的处理脚本
        "终极合并所有16模块补充数据.py",
        "终极合并所有20模块补充数据.py",
        "终极合并所有补充数据.py",
        
        # 过时的验证脚本
        "最终前端数据验证.py",
        "最终系统验证.py",
        "最终词典验证.py",
        "最终验证8个Label.py",
        "最终验证修复效果.py",
        
        # 重复的检查脚本
        "检查neo4j实际数据.py",
        "检查前端数据显示问题.py",
        "检查并重启所有后端服务.py",
        "检查服务状态_简化版.py",
    ]
    
    for file in duplicate_files:
        if os.path.exists(file):
            # 备份
            shutil.copy2(file, backup_dir)
            # 删除
            os.remove(file)
            print(f"   ✅ 删除重复文件: {file}")
            cleanup_count += 1
    
    # 3. 移动剩余的测试文件到测试目录
    print(f"\n📁 移动剩余测试文件...")
    
    test_files = [
        "test_display_fix.py",
        "test_doc_parsing.py", 
        "test_doc_parsing_final.py",
        "test_document_parsing.py",
        "test_document_parsing_fix.py",
        "test_excel_timestamp_fix.py",
        "test_frontend_fixes.py",
        "test_graph_api.py",
        "test_graph_api_fix.py",
        "test_graph_query.py",
        "test_neo4j_connection.py",
        "test_parsing_with_logs.py",
        "test_pdf.py",
        "test_prompt_integration.py",
        "test_simple_doc.py",
        "test_system_management.py",
    ]
    
    os.makedirs("tests/legacy", exist_ok=True)
    
    for file in test_files:
        if os.path.exists(file):
            target_path = f"tests/legacy/{file}"
            if not os.path.exists(target_path):
                shutil.move(file, target_path)
                print(f"   📂 移动测试文件: {file} -> tests/legacy/")
                cleanup_count += 1
    
    # 4. 移动剩余的脚本文件
    print(f"\n📁 移动剩余脚本文件...")
    
    script_files = [
        "测试API和前端.py",
        "测试API调用.py", 
        "测试neo4j连接.py",
        "测试前端API调用.py",
        "测试前端修复.html",
        "测试图谱API.py",
        "测试图谱功能修复.py",
        "测试图谱可视化.py",
        "测试数据治理功能.py",
        "测试系统管理功能.py",
        "测试词典API.py",
        "测试词典API修复.py",
    ]
    
    for file in script_files:
        if os.path.exists(file):
            target_path = f"scripts/legacy/{file}"
            if not os.path.exists(target_path):
                shutil.move(file, target_path)
                print(f"   📂 移动脚本文件: {file} -> scripts/legacy/")
                cleanup_count += 1
    
    # 5. 清理空目录
    print(f"\n🧽 清理空目录...")
    empty_dirs_removed = 0
    for root, dirs, files in os.walk('.', topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"   🗂️ 删除空目录: {dir_path}")
                    empty_dirs_removed += 1
            except OSError:
                pass
    
    # 6. 生成清理报告
    print(f"\n📊 最终清理统计")
    print("=" * 60)
    print(f"🗑️ 清理文件数: {cleanup_count}")
    print(f"🗂️ 删除空目录数: {empty_dirs_removed}")
    print(f"📦 备份位置: {backup_dir}")
    
    # 显示清理后的根目录统计
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    py_files = [f for f in root_files if f.endswith('.py')]
    config_files = [f for f in root_files if f.endswith(('.yml', '.yaml', '.json', '.conf'))]
    doc_files = [f for f in root_files if f.endswith(('.md', '.txt'))]
    data_files = [f for f in root_files if f.endswith(('.csv', '.xlsx', '.cypher'))]
    
    print(f"\n📁 最终根目录统计:")
    print(f"   Python脚本: {len(py_files)} 个")
    print(f"   配置文件: {len(config_files)} 个")
    print(f"   文档文件: {len(doc_files)} 个")
    print(f"   数据文件: {len(data_files)} 个")
    print(f"   总文件数: {len(root_files)} 个")
    
    return {
        "cleanup_count": cleanup_count,
        "empty_dirs_removed": empty_dirs_removed,
        "backup_dir": backup_dir,
        "final_stats": {
            "python_files": len(py_files),
            "config_files": len(config_files),
            "doc_files": len(doc_files),
            "data_files": len(data_files),
            "total_files": len(root_files)
        }
    }

def main():
    """主函数"""
    print("🔧 执行最终清理")
    print("=" * 80)
    
    try:
        # 执行清理
        result = execute_final_cleanup()
        
        print(f"\n✅ 最终清理完成!")
        print(f"🎯 清理效果:")
        print(f"   - 清理了 {result['cleanup_count']} 个文件")
        print(f"   - 删除了 {result['empty_dirs_removed']} 个空目录")
        print(f"   - 根目录现有 {result['final_stats']['total_files']} 个文件")
        
        print(f"\n🎉 目录优化完成!")
        print(f"   📁 目录结构更加清晰")
        print(f"   🔧 核心文件更加突出")
        print(f"   🚀 系统更易维护")
        
    except Exception as e:
        print(f"❌ 清理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
