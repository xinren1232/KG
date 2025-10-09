#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
彻底清理冗余文件 - 删除所有临时、测试、指导和冗余文件
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def check_empty_or_minimal_files():
    """检查空文件或只有简单内容的文件"""
    print("🔍 检查空文件和最小内容文件...")
    
    empty_files = []
    root_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.py')]
    
    for file in root_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                lines = content.split('\n')
                
            # 检查是否为空文件或只有简单注释
            if (not content or 
                content == '#' or 
                len(lines) <= 3 or
                (len(lines) <= 5 and all(line.strip().startswith('#') or not line.strip() for line in lines))):
                empty_files.append(file)
                print(f"   📄 发现空/最小文件: {file}")
        except Exception as e:
            print(f"   ⚠️ 无法读取文件 {file}: {e}")
    
    return empty_files

def identify_all_redundant_files():
    """识别所有冗余文件"""
    print("\n🔍 识别所有冗余和临时文件...")
    
    redundant_files = []
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    # 测试文件模式
    test_patterns = [
        'test_', '测试', 'debug_', 'verify_', '验证', '检查',
        'final_', '最终', 'simple_', 'temp_', 'tmp_'
    ]
    
    # 指导文件模式
    guide_patterns = [
        '指南', '手册', '说明', 'guide', 'manual', '步骤', '执行'
    ]
    
    # 报告文件模式
    report_patterns = [
        '报告', 'report', '总结', 'summary', '完成', '修复'
    ]
    
    # 临时脚本模式
    temp_script_patterns = [
        '快速', '临时', '立即', '直接', '简单', '彻底'
    ]
    
    for file in root_files:
        file_lower = file.lower()
        
        # 检查测试文件
        if any(pattern in file for pattern in test_patterns):
            redundant_files.append(('测试文件', file))
        
        # 检查指导文件
        elif any(pattern in file for pattern in guide_patterns) and file.endswith('.md'):
            redundant_files.append(('指导文件', file))
        
        # 检查报告文件
        elif any(pattern in file for pattern in report_patterns) and file.endswith(('.md', '.json')):
            redundant_files.append(('报告文件', file))
        
        # 检查临时脚本
        elif any(pattern in file for pattern in temp_script_patterns) and file.endswith('.py'):
            redundant_files.append(('临时脚本', file))
        
        # 检查重复的数据文件
        elif ('硬件模块' in file or '批次' in file or '补充' in file) and file.endswith(('.cypher', '.json', '.csv')):
            redundant_files.append(('重复数据文件', file))
    
    # 按类型分组显示
    by_type = {}
    for file_type, file_name in redundant_files:
        if file_type not in by_type:
            by_type[file_type] = []
        by_type[file_type].append(file_name)
    
    for file_type, files in by_type.items():
        print(f"   📂 {file_type} ({len(files)}个):")
        for file in files[:10]:  # 显示前10个
            print(f"      - {file}")
        if len(files) > 10:
            print(f"      ... 还有{len(files)-10}个文件")
    
    return [file for _, file in redundant_files]

def execute_thorough_cleanup():
    """执行彻底清理"""
    print("🧹 执行彻底清理")
    print("=" * 80)
    
    # 创建彻底清理备份
    backup_dir = f"thorough_cleanup_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    print(f"📦 创建彻底清理备份: {backup_dir}")
    
    cleanup_count = 0
    
    # 1. 删除已清空的文件
    print(f"\n🗑️ 删除已清空的文件...")
    empty_files = check_empty_or_minimal_files()
    
    for file in empty_files:
        if os.path.exists(file):
            # 备份
            shutil.copy2(file, backup_dir)
            # 删除
            os.remove(file)
            print(f"   ✅ 删除空文件: {file}")
            cleanup_count += 1
    
    # 2. 删除所有冗余文件
    print(f"\n🗑️ 删除所有冗余文件...")
    redundant_files = identify_all_redundant_files()
    
    for file in redundant_files:
        if os.path.exists(file):
            # 备份
            shutil.copy2(file, backup_dir)
            # 删除
            os.remove(file)
            print(f"   ✅ 删除冗余文件: {file}")
            cleanup_count += 1
    
    # 3. 删除明确的冗余文件列表
    print(f"\n🗑️ 删除明确的冗余文件...")
    
    explicit_redundant_files = [
        # 所有测试相关文件
        "测试API和前端.py", "测试API调用.py", "测试neo4j连接.py",
        "测试前端API调用.py", "测试前端修复.html", "测试图谱API.py",
        "测试图谱功能修复.py", "测试图谱可视化.py", "测试数据治理功能.py",
        "测试系统管理功能.py", "测试词典API.py", "测试词典API修复.py",
        
        # 所有验证相关文件
        "验证修复效果.py", "验证图谱导入.py", "验证图谱更新结果.py",
        "验证数据更新.py", "最终验证修复效果.py", "最终验证8个Label.py",
        "最终系统验证.py", "最终词典验证.py", "最终前端数据验证.py",
        
        # 所有检查相关文件
        "检查服务状态.py", "检查服务状态_简化版.py", "检查neo4j实际数据.py",
        "检查前端数据显示问题.py", "检查并重启所有后端服务.py",
        "检查词典数据路径.py", "检查图谱状态.py", "检查图谱数据质量.py",
        
        # 所有debug相关文件
        "debug_api_query.py", "debug_timestamp_issue.py", "debug_parsing_issue.py",
        
        # 所有final相关文件
        "final_test.py", "final_system_test.py",
        
        # 所有指南和说明文件
        "API服务重启指南.md", "API端点修复建议.md", "API调用修复指南.md",
        "Neo4j启动指南.md", "Neo4j图谱数据导入指南.md", "Neo4j手动导入指南.md",
        "Neo4j执行步骤.md", "Neo4j空标签清理说明.md", "手动重启Neo4j指南.md",
        "install_neo4j_guide.md", "local_dev_setup.md",
        
        # 所有报告文件
        "BACKEND_STARTUP_SUCCESS.md", "DICTIONARY_REAL_DATA_FIX_REPORT.md",
        "FRONTEND_DICTIONARY_FIX_REPORT.md", "FRONTEND_FIXES_SUMMARY.md",
        "GRAPH_DATA_CONSISTENCY_FIX_REPORT.md", "GRAPH_STATS_FIX_REPORT.md",
        "GRAPH_VISUALIZATION_FIX_REPORT.md", "REAL_BUSINESS_DATA_FIX_REPORT.md",
        "REAL_DATA_VERIFICATION_REPORT.md", "UNIQUE_PATH_CLEANUP_REPORT.md",
        "标签规则页面删除完成报告.md", "服务状态检查报告.md",
        
        # 所有总结文件
        "词典图谱数据更新完成总结.md", "目录清理完成总结报告.md",
        "目录清理验证报告.md", "最终清理完成报告.md",
        
        # 所有快速/临时脚本
        "快速启动API.py", "快速处理补充数据.py", "快速重建图谱数据.py",
        "快速验证API数据.py", "立即修复数据模型不一致.py", "直接执行图谱更新.py",
        "彻底清理标签.py", "彻底清理空标签.py", "简化数据导入.py", "简单验证.py",
        
        # 所有分析和检查脚本
        "全面数据设计排查.py", "全面检查词典数据.py", "分析当前数据质量.py",
        "数据模型不一致问题分析.py", "服务器部署前系统全面检查.py",
        "数据保存形式优化方案.py", "词典数据可视化分析.py", "词典数据统计分析.py",
        
        # 所有修复脚本
        "修复词典数据格式.py", "修复关系创建.py", "恢复图谱关系.py",
        
        # 所有导入和更新脚本
        "导入补充数据.py", "通过API导入补充数据.py", "更新图谱数据.py",
        "更新统一词典数据.py", "数据迁移汇总更新.py", "补充图谱数据.py",
        "统一汇总所有词典数据.py", "自动重建图谱数据.py", "清理并重建图谱数据.py",
        "生成关系并验证.py", "生成分批导入命令.py", "建立模块分组并联接.py",
        
        # 所有清理脚本
        "清理多余标签.py", "通过查询清理空标签.py", "确保路径唯一性.py",
        "精确目录清理.py", "执行最终清理.py", "目录清理分析报告.py",
        
        # 所有启动脚本
        "启动Neo4j.py", "启动前端.py", "启动并检查所有服务.py",
        "全面重启所有服务.bat", "start_frontend.bat",
        
        # 所有数据文件
        "全部硬件模块数据导入脚本.cypher", "全部硬件模块数据统计报告.json",
        "完整分批导入命令.cypher", "快速更新图谱.cypher", "数据模型修复.cypher",
        "补充导入剩余数据.cypher", "补充数据导入脚本.cypher", "词典数据图谱更新脚本.cypher",
        "数据补全模板.csv", "来料问题洗后版.xlsx",
        
        # 所有配置和报告JSON
        "目录清理分析报告.json", "目录清理报告.json",
        
        # 所有Prompt和指南文件
        "优化后的词典抽取Prompt.md", "词典抽取Prompt_简化版.md",
        "词典抽取Prompt优化对比.md", "词典抽取Prompt前端集成完成报告.md",
        "词典质量检查Prompt使用指南.md", "词典质量检查Prompt集成完成报告.md",
        "词典质量检查工具.py", "词典质量检查报告.md",
        "词典图谱设计规范.md", "前端数据更新指南.md", "图谱更新完整指南.md",
        "分批导入执行指南.md", "用户操作手册.md",
        
        # 所有README文件
        "README_关系导入.md",
        
        # 其他脚本
        "check_vue_components.py", "clean_and_reimport.py",
        "import_relations_from_csv.py", "系统状态总结.py",
        "系统状态检查和更新.py", "执行图谱更新_正确密码.py",
        "执行终极数据导入.py", "目录清理脚本.sh",
    ]
    
    for file in explicit_redundant_files:
        if os.path.exists(file):
            # 备份
            shutil.copy2(file, backup_dir)
            # 删除
            os.remove(file)
            print(f"   ✅ 删除明确冗余文件: {file}")
            cleanup_count += 1
    
    # 4. 清理空目录
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
    
    # 5. 生成清理报告
    print(f"\n📊 彻底清理统计")
    print("=" * 80)
    print(f"🗑️ 清理文件数: {cleanup_count}")
    print(f"🗂️ 删除空目录数: {empty_dirs_removed}")
    print(f"📦 备份位置: {backup_dir}")
    
    # 显示清理后的根目录统计
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    py_files = [f for f in root_files if f.endswith('.py')]
    config_files = [f for f in root_files if f.endswith(('.yml', '.yaml', '.json', '.conf', '.sh'))]
    doc_files = [f for f in root_files if f.endswith(('.md', '.txt'))]
    data_files = [f for f in root_files if f.endswith(('.csv', '.xlsx', '.cypher'))]
    other_files = [f for f in root_files if not any(f.endswith(ext) for ext in ['.py', '.yml', '.yaml', '.json', '.conf', '.sh', '.md', '.txt', '.csv', '.xlsx', '.cypher'])]
    
    print(f"\n📁 彻底清理后根目录统计:")
    print(f"   Python脚本: {len(py_files)} 个")
    print(f"   配置文件: {len(config_files)} 个")
    print(f"   文档文件: {len(doc_files)} 个")
    print(f"   数据文件: {len(data_files)} 个")
    print(f"   其他文件: {len(other_files)} 个")
    print(f"   总文件数: {len(root_files)} 个")
    
    # 显示保留的核心文件
    print(f"\n📋 保留的核心文件:")
    core_files = [
        "README.md", "LICENSE", "docker-compose.yml", "docker-compose.prod.yml",
        "Dockerfile.api", "部署脚本.sh", "全面重启所有服务.py",
        "服务状态检查.py", "完整部署优化方案.md", "系统优化总结报告.md"
    ]
    
    for file in core_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (不存在)")
    
    return {
        "cleanup_count": cleanup_count,
        "empty_dirs_removed": empty_dirs_removed,
        "backup_dir": backup_dir,
        "final_stats": {
            "python_files": len(py_files),
            "config_files": len(config_files),
            "doc_files": len(doc_files),
            "data_files": len(data_files),
            "other_files": len(other_files),
            "total_files": len(root_files)
        }
    }

def main():
    """主函数"""
    print("🔧 执行彻底清理")
    print("=" * 80)
    
    try:
        # 执行清理
        result = execute_thorough_cleanup()
        
        print(f"\n✅ 彻底清理完成!")
        print(f"🎯 清理效果:")
        print(f"   - 清理了 {result['cleanup_count']} 个文件")
        print(f"   - 删除了 {result['empty_dirs_removed']} 个空目录")
        print(f"   - 根目录现有 {result['final_stats']['total_files']} 个文件")
        
        print(f"\n🎉 目录彻底优化完成!")
        print(f"   📁 目录结构极度简洁")
        print(f"   🔧 只保留核心文件")
        print(f"   🚀 系统高度优化")
        
    except Exception as e:
        print(f"❌ 清理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
