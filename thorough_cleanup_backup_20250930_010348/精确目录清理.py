#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确目录清理脚本
安全地清理重复、多余和冲突的文件
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def create_backup():
    """创建备份目录"""
    backup_dir = f"cleanup_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    print(f"📦 创建备份目录: {backup_dir}")
    return backup_dir

def safe_remove_files(files_to_remove, backup_dir):
    """安全删除文件（先备份）"""
    print(f"\n🗑️ 删除重复和临时文件...")
    
    removed_count = 0
    for file in files_to_remove:
        if os.path.exists(file):
            # 备份文件
            backup_path = os.path.join(backup_dir, "removed_files")
            os.makedirs(backup_path, exist_ok=True)
            shutil.copy2(file, backup_path)
            
            # 删除原文件
            os.remove(file)
            print(f"   ✅ 删除: {file}")
            removed_count += 1
    
    print(f"📊 共删除 {removed_count} 个文件")
    return removed_count

def organize_files_to_directories(file_moves, backup_dir):
    """整理文件到相应目录"""
    print(f"\n📁 整理文件到子目录...")
    
    moved_count = 0
    for target_dir, files in file_moves.items():
        if files:
            # 创建目标目录
            os.makedirs(target_dir, exist_ok=True)
            
            for file in files:
                if os.path.exists(file):
                    # 备份原文件位置信息
                    backup_info = os.path.join(backup_dir, "moved_files_info.txt")
                    with open(backup_info, "a", encoding="utf-8") as f:
                        f.write(f"{file} -> {target_dir}/{os.path.basename(file)}\n")
                    
                    # 移动文件
                    target_path = os.path.join(target_dir, os.path.basename(file))
                    if not os.path.exists(target_path):
                        shutil.move(file, target_path)
                        print(f"   📂 移动: {file} -> {target_dir}/")
                        moved_count += 1
                    else:
                        print(f"   ⚠️ 跳过: {file} (目标已存在)")
    
    print(f"📊 共移动 {moved_count} 个文件")
    return moved_count

def cleanup_directory():
    """执行目录清理"""
    print("🧹 开始精确目录清理")
    print("=" * 60)
    
    # 创建备份
    backup_dir = create_backup()
    
    # 1. 明确要删除的文件列表
    files_to_remove = [
        # 临时测试文件
        "simple_test.doc", "simple_test.docx", "simple_test.txt", 
        "simple_test.xlsx", "simple_test_debug.txt", "test.docx",
        
        # 旧备份文件
        "graph_backup_20250928_110602.json", "backup_data.sh",
        
        # 重复的启动脚本
        "启动API服务.bat", "启动所有服务.bat", "快速修复并启动.bat",
        
        # 重复的检查脚本
        "check_api_status.py", "check_neo4j_data.py", "check_node_structure.py",
        "comprehensive_system_check.py",
        
        # 重复的修复脚本
        "修复API查询逻辑.py", "修复Label分类.py", "修复neo4j显示.py",
        "修复neo4j连接.py", "修复关系创建.py", "修复前端错误.py",
        
        # 重复的测试文件
        "test_hardware_report.doc", "test_hardware_report.docx",
        "test_quality_analysis.pdf", "test_quality_report.pdf",
        "test_report.docx", "test_simple.txt", "test_text_parsing.txt",
        "test_word_parsing.docx",
        
        # 重复的验证脚本
        "verify_doc_fix.py", "verify_timestamp_fix.py",
        "simple_api_test.py", "final_test.py",
        
        # 过时的数据处理脚本
        "append_dictionary_data.py", "append_new_dictionary_data.py",
        "cleanup_duplicate_dictionary_files.py",
        
        # 重复的Neo4j脚本
        "彻底修复neo4j显示问题.py", "解决neo4j认证问题.py",
        "重置Neo4j密码.py", "等待并重试Neo4j连接.py",
    ]
    
    # 2. 文件移动规则
    file_moves = {
        "reports/legacy": [
            # 移动报告文件
            "ALL_SERVICES_STATUS_REPORT.md", "API_422_ERROR_FIX_REPORT.md",
            "BACKEND_SERVICE_STATUS.md", "COMPREHENSIVE_SYSTEM_REPORT.md",
            "COMPLETE_DICTIONARY_FIX_REPORT.md", "DICTIONARY_DISPLAY_FIX_REPORT.md",
            "FINAL_GRAPH_STATS_FIX_REPORT.md", "FINAL_VUE_OPTIMIZATION_REPORT.md",
            "GRAPH_DATA_FIX_REPORT.md", "NEO4J_RESTART_REPORT.md",
            "VUE_OPTIMIZATION_REPORT.md", "FINAL_OPTIMIZATION_SUMMARY.md",
            
            # 移动总结文档
            "Neo4j分类显示问题修复完成总结.md", "前端重新设计完成总结.md",
            "图谱可视化重新设计完成总结.md", "数据治理重新设计完成总结.md",
            "系统管理页面重新设计完成总结.md", "标签规则合并完成报告.md",
            "导航菜单清理完成报告.md", "硬件模块扩展总结.md",
        ],
        
        "scripts/legacy": [
            # 移动旧脚本
            "debug_api_query.py", "debug_parsing_issue.py", "debug_timestamp_issue.py",
            "fix_api_issues.py", "fix_labels.py", "optimize_vue_warnings.py",
            "promote_suggestions_to_templates.py", "suggest_relations.py",
            "validate_relations.py", "comprehensive_vue_fix.py",
            
            # 移动检查脚本
            "检查图谱数据结构.py", "检查图谱数据质量.py", "检查图谱状态.py",
            "检查当前数据状态.py", "检查数据格式.py", "检查词典数据路径.py",
            "深度检查数据一致性.py",
        ],
        
        "data/import/legacy": [
            # 移动批次导入文件
            "导入批次_01.cypher", "导入批次_02.cypher", "导入批次_03.cypher",
            "导入批次_04.cypher", "导入批次_05.cypher", "导入批次_06.cypher",
            "导入批次_07.cypher", "导入批次_08.cypher", "导入批次_09.cypher",
            "导入批次_10.cypher", "导入批次_11.cypher", "导入批次_12.cypher",
            "导入批次_13.cypher", "导入批次_14.cypher",
            
            # 移动合并脚本
            "合并全部12个硬件模块数据.py", "合并全部16个硬件模块数据.py",
            "合并全部20个硬件模块数据.py", "合并全部硬件模块数据.py",
            "合并所有补充数据.py", "最终合并所有补充数据.py",
            
            # 移动处理脚本
            "处理新增硬件模块数据.py", "处理硬件模块数据.py",
            "处理第三批硬件模块数据.py", "处理第四批硬件模块数据.py",
            "处理第五批硬件模块数据.py",
        ],
        
        "data/dictionary/modules": [
            # 移动硬件模块词典数据
            "硬件模块词典数据_主板PCBA.csv", "硬件模块词典数据_传感器.csv",
            "硬件模块词典数据_充电电源.csv", "硬件模块词典数据_先进制造工艺.csv",
            "硬件模块词典数据_声学.csv", "硬件模块词典数据_外壳涂层.csv",
            "硬件模块词典数据_失效分析可靠性.csv", "硬件模块词典数据_射频天线.csv",
            "硬件模块词典数据_接口连接器.csv", "硬件模块词典数据_摄像头.csv",
            "硬件模块词典数据_散热系统.csv", "硬件模块词典数据_显示屏.csv",
            "硬件模块词典数据_材料科学基础.csv", "硬件模块词典数据_标准法规.csv",
            "硬件模块词典数据_生产测试治具.csv", "硬件模块词典数据_电池.csv",
            "硬件模块词典数据_结构连接器.csv", "硬件模块词典数据_被动元件.csv",
            "硬件模块词典数据_连接网络.csv", "硬件模块词典数据_马达触觉.csv",
        ],
        
        "config/legacy": [
            # 移动配置和报告JSON文件
            "Label分类修复报告.json", "prompt_integration_report.json",
            "system_test_report.json", "图谱功能修复验证结果.json",
            "最终词典验证结果.json", "词典API测试结果.json",
            "前端数据显示问题检查报告.json", "前端错误修复报告.json",
            "词典数据修复报告.json", "词典数据全面检查报告.json",
            "数据治理功能测试报告.json", "系统管理功能测试报告.json",
        ]
    }
    
    # 3. 执行删除操作
    removed_count = safe_remove_files(files_to_remove, backup_dir)
    
    # 4. 执行文件移动操作
    moved_count = organize_files_to_directories(file_moves, backup_dir)
    
    # 5. 清理空目录
    print(f"\n🧽 清理空目录...")
    empty_dirs_removed = 0
    for root, dirs, files in os.walk('.', topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):  # 空目录
                    os.rmdir(dir_path)
                    print(f"   🗂️ 删除空目录: {dir_path}")
                    empty_dirs_removed += 1
            except OSError:
                pass  # 目录不为空或无权限
    
    # 6. 生成清理报告
    print(f"\n📊 清理完成统计")
    print("=" * 60)
    print(f"🗑️ 删除文件数: {removed_count}")
    print(f"📂 移动文件数: {moved_count}")
    print(f"🗂️ 删除空目录数: {empty_dirs_removed}")
    print(f"📦 备份位置: {backup_dir}")
    
    # 7. 显示清理后的根目录统计
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    py_files = [f for f in root_files if f.endswith('.py')]
    config_files = [f for f in root_files if f.endswith(('.yml', '.yaml', '.json', '.conf'))]
    doc_files = [f for f in root_files if f.endswith(('.md', '.txt'))]
    
    print(f"\n📁 清理后根目录统计:")
    print(f"   Python脚本: {len(py_files)} 个")
    print(f"   配置文件: {len(config_files)} 个")
    print(f"   文档文件: {len(doc_files)} 个")
    print(f"   总文件数: {len(root_files)} 个")
    
    # 8. 保存清理报告
    cleanup_report = {
        "清理时间": datetime.now().isoformat(),
        "删除文件数": removed_count,
        "移动文件数": moved_count,
        "删除空目录数": empty_dirs_removed,
        "备份位置": backup_dir,
        "清理后统计": {
            "Python脚本": len(py_files),
            "配置文件": len(config_files),
            "文档文件": len(doc_files),
            "总文件数": len(root_files)
        }
    }
    
    import json
    with open("目录清理报告.json", "w", encoding="utf-8") as f:
        json.dump(cleanup_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 清理报告已保存: 目录清理报告.json")
    
    return cleanup_report

def main():
    """主函数"""
    print("🔧 精确目录清理工具")
    print("=" * 80)
    
    # 确认操作
    print("⚠️ 此操作将删除和移动大量文件")
    print("📦 所有操作都会先创建备份")
    
    try:
        # 执行清理
        report = cleanup_directory()
        
        print(f"\n✅ 目录清理完成!")
        print(f"🎯 建议下一步:")
        print(f"   1. 检查清理结果是否符合预期")
        print(f"   2. 测试系统功能是否正常")
        print(f"   3. 如果确认无误，可删除备份目录")
        print(f"   4. 提交清理后的代码到版本控制")
        
    except Exception as e:
        print(f"❌ 清理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
