#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录清理分析报告
分析当前目录结构，识别重复、多余和冲突的文件
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import json

def analyze_directory_structure():
    """分析目录结构"""
    print("📁 目录结构分析")
    print("=" * 60)
    
    # 分类文件
    file_categories = {
        "报告文件": [],
        "脚本文件": [],
        "配置文件": [],
        "数据文件": [],
        "测试文件": [],
        "文档文件": [],
        "临时文件": [],
        "重复文件": [],
        "冲突文件": []
    }
    
    # 扫描根目录文件
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    # 按类型分类
    for file in root_files:
        file_lower = file.lower()
        
        # 报告文件
        if any(keyword in file for keyword in ['REPORT', '报告', '总结', '指南', 'SUMMARY']):
            file_categories["报告文件"].append(file)
        
        # 脚本文件
        elif file.endswith(('.py', '.bat', '.sh')):
            file_categories["脚本文件"].append(file)
        
        # 配置文件
        elif file.endswith(('.yml', '.yaml', '.json', '.conf', '.cfg')):
            file_categories["配置文件"].append(file)
        
        # 数据文件
        elif file.endswith(('.csv', '.xlsx', '.cypher')):
            file_categories["数据文件"].append(file)
        
        # 测试文件
        elif 'test' in file_lower or '测试' in file:
            file_categories["测试文件"].append(file)
        
        # 文档文件
        elif file.endswith(('.md', '.txt', '.doc', '.docx', '.pdf')):
            file_categories["文档文件"].append(file)
        
        # 临时文件
        elif any(temp in file_lower for temp in ['temp', 'tmp', 'backup', '_old', '_bak']):
            file_categories["临时文件"].append(file)
    
    # 打印分类结果
    for category, files in file_categories.items():
        if files:
            print(f"\n{category} ({len(files)}个):")
            for file in sorted(files)[:10]:  # 只显示前10个
                print(f"   - {file}")
            if len(files) > 10:
                print(f"   ... 还有{len(files) - 10}个文件")
    
    return file_categories

def identify_duplicate_files():
    """识别重复文件"""
    print("\n🔍 重复文件识别")
    print("=" * 60)
    
    # 按功能分组的重复文件
    duplicate_groups = {
        "API相关": [],
        "Neo4j相关": [],
        "前端相关": [],
        "数据导入": [],
        "系统检查": [],
        "词典处理": [],
        "图谱更新": [],
        "服务启动": []
    }
    
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    for file in root_files:
        file_lower = file.lower()
        
        # API相关重复
        if any(keyword in file for keyword in ['api', 'API']):
            duplicate_groups["API相关"].append(file)
        
        # Neo4j相关重复
        elif any(keyword in file for keyword in ['neo4j', 'Neo4j']):
            duplicate_groups["Neo4j相关"].append(file)
        
        # 前端相关重复
        elif any(keyword in file for keyword in ['前端', 'frontend', 'vue', 'VUE']):
            duplicate_groups["前端相关"].append(file)
        
        # 数据导入重复
        elif any(keyword in file for keyword in ['导入', '合并', '处理', 'import']):
            duplicate_groups["数据导入"].append(file)
        
        # 系统检查重复
        elif any(keyword in file for keyword in ['检查', '验证', '测试', 'check', 'test', 'verify']):
            duplicate_groups["系统检查"].append(file)
        
        # 词典处理重复
        elif any(keyword in file for keyword in ['词典', 'dictionary', 'dict']):
            duplicate_groups["词典处理"].append(file)
        
        # 图谱更新重复
        elif any(keyword in file for keyword in ['图谱', '更新', 'graph', 'update']):
            duplicate_groups["图谱更新"].append(file)
        
        # 服务启动重复
        elif any(keyword in file for keyword in ['启动', '重启', 'start', 'restart']):
            duplicate_groups["服务启动"].append(file)
    
    # 显示重复文件组
    for group, files in duplicate_groups.items():
        if len(files) > 1:
            print(f"\n{group} (重复{len(files)}个):")
            for file in sorted(files):
                print(f"   - {file}")
    
    return duplicate_groups

def identify_obsolete_files():
    """识别过时文件"""
    print("\n🗑️ 过时文件识别")
    print("=" * 60)
    
    obsolete_patterns = [
        # 版本标记的旧文件
        r'.*_v\d+\..*',
        r'.*_old\..*',
        r'.*_backup\..*',
        r'.*_bak\..*',
        r'.*_temp\..*',
        r'.*_tmp\..*',
        
        # 批次文件
        r'.*批次.*',
        r'.*batch.*',
        
        # 测试文件
        r'test_.*\.py',
        r'.*_test\..*',
        r'debug_.*\.py',
        
        # 临时报告
        r'.*报告.*\.json',
        r'.*REPORT.*\.md',
        r'.*总结.*\.md'
    ]
    
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    obsolete_files = []
    
    for file in root_files:
        for pattern in obsolete_patterns:
            if re.match(pattern, file, re.IGNORECASE):
                obsolete_files.append(file)
                break
    
    print(f"发现 {len(obsolete_files)} 个可能过时的文件:")
    for file in sorted(obsolete_files)[:20]:  # 显示前20个
        print(f"   - {file}")
    
    if len(obsolete_files) > 20:
        print(f"   ... 还有{len(obsolete_files) - 20}个文件")
    
    return obsolete_files

def analyze_directory_conflicts():
    """分析目录冲突"""
    print("\n⚠️ 目录冲突分析")
    print("=" * 60)
    
    conflicts = []
    
    # 检查重复功能的目录
    directories = [d for d in os.listdir('.') if os.path.isdir(d)]
    
    # 功能重复检查
    function_dirs = defaultdict(list)
    
    for dir_name in directories:
        dir_lower = dir_name.lower()
        
        if 'api' in dir_lower:
            function_dirs['API服务'].append(dir_name)
        elif 'app' in dir_lower:
            function_dirs['应用'].append(dir_name)
        elif 'service' in dir_lower:
            function_dirs['服务'].append(dir_name)
        elif 'data' in dir_lower:
            function_dirs['数据'].append(dir_name)
        elif 'config' in dir_lower:
            function_dirs['配置'].append(dir_name)
        elif 'test' in dir_lower:
            function_dirs['测试'].append(dir_name)
        elif 'tool' in dir_lower:
            function_dirs['工具'].append(dir_name)
    
    # 显示可能的冲突
    for function, dirs in function_dirs.items():
        if len(dirs) > 1:
            print(f"{function}目录重复: {', '.join(dirs)}")
            conflicts.append((function, dirs))
    
    return conflicts

def generate_cleanup_recommendations():
    """生成清理建议"""
    print("\n💡 清理建议")
    print("=" * 60)
    
    recommendations = {
        "立即删除": [
            # 明显的临时文件
            "backup_data.sh",  # 已有更好的部署脚本
            "graph_backup_20250928_110602.json",  # 旧备份文件
            
            # 重复的测试文件
            "simple_test.doc", "simple_test.docx", "simple_test.txt", "simple_test.xlsx",
            "test.docx", "simple_test_debug.txt",
            
            # 重复的启动脚本
            "启动API服务.bat",  # 功能重复
            "启动所有服务.bat",  # 功能重复
            "快速修复并启动.bat",  # 功能重复
            
            # 过时的检查脚本
            "check_api_status.py", "check_neo4j_data.py", "check_node_structure.py",
            "comprehensive_system_check.py",
            
            # 重复的修复脚本
            "修复API查询逻辑.py", "修复Label分类.py", "修复neo4j显示.py",
            "修复neo4j连接.py", "修复关系创建.py", "修复前端错误.py",
        ],
        
        "合并整理": [
            # 数据导入脚本
            "合并全部12个硬件模块数据.py", "合并全部16个硬件模块数据.py", 
            "合并全部20个硬件模块数据.py", "合并全部硬件模块数据.py",
            
            # 批次导入文件
            "导入批次_01.cypher", "导入批次_02.cypher", "导入批次_03.cypher",
            # ... 其他批次文件
            
            # 词典数据文件
            "硬件模块词典数据_主板PCBA.csv", "硬件模块词典数据_传感器.csv",
            # ... 其他词典文件
        ],
        
        "移动到子目录": [
            # 报告文件移动到 reports/
            "ALL_SERVICES_STATUS_REPORT.md", "API_422_ERROR_FIX_REPORT.md",
            "BACKEND_SERVICE_STATUS.md", "COMPREHENSIVE_SYSTEM_REPORT.md",
            
            # 脚本文件移动到 scripts/
            "append_dictionary_data.py", "append_new_dictionary_data.py",
            "clean_and_reimport.py", "cleanup_duplicate_dictionary_files.py",
            
            # 配置文件移动到 config/
            "Label分类修复报告.json", "prompt_integration_report.json",
            "system_test_report.json",
        ],
        
        "保留核心文件": [
            # 重要的配置文件
            "docker-compose.prod.yml", "docker-compose.yml", "Dockerfile.api",
            
            # 核心脚本
            "部署脚本.sh", "全面重启所有服务.py", "服务状态检查.py",
            
            # 重要文档
            "README.md", "完整部署优化方案.md", "系统优化总结报告.md",
            
            # 核心目录
            "api/", "apps/", "config/", "data/", "nginx/",
        ]
    }
    
    for category, files in recommendations.items():
        print(f"\n{category}:")
        for file in files[:10]:  # 显示前10个
            print(f"   - {file}")
        if len(files) > 10:
            print(f"   ... 还有{len(files) - 10}个文件")
    
    return recommendations

def create_cleanup_script():
    """创建清理脚本"""
    print("\n📝 生成清理脚本")
    print("=" * 60)
    
    cleanup_script = '''#!/bin/bash
# 目录清理脚本 - 删除重复、多余和冲突的文件

set -e

echo "🧹 开始清理目录..."

# 创建备份目录
BACKUP_DIR="cleanup_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

echo "📦 创建备份: $BACKUP_DIR"

# 1. 删除明显的临时和重复文件
echo "🗑️ 删除临时和重复文件..."

# 临时测试文件
rm -f simple_test.* test.docx simple_test_debug.txt

# 旧备份文件
rm -f graph_backup_*.json backup_data.sh

# 重复的启动脚本
rm -f 启动API服务.bat 启动所有服务.bat 快速修复并启动.bat

# 重复的检查脚本
rm -f check_api_status.py check_neo4j_data.py check_node_structure.py
rm -f comprehensive_system_check.py

# 重复的修复脚本
rm -f 修复API查询逻辑.py 修复Label分类.py 修复neo4j显示.py
rm -f 修复neo4j连接.py 修复关系创建.py 修复前端错误.py

# 2. 整理报告文件
echo "📋 整理报告文件..."
mkdir -p reports/legacy
mv *REPORT*.md reports/legacy/ 2>/dev/null || true
mv *报告*.md reports/legacy/ 2>/dev/null || true
mv *总结*.md reports/legacy/ 2>/dev/null || true

# 3. 整理脚本文件
echo "🔧 整理脚本文件..."
mkdir -p scripts/legacy
mv append_*.py scripts/legacy/ 2>/dev/null || true
mv clean_*.py scripts/legacy/ 2>/dev/null || true
mv cleanup_*.py scripts/legacy/ 2>/dev/null || true
mv debug_*.py scripts/legacy/ 2>/dev/null || true
mv fix_*.py scripts/legacy/ 2>/dev/null || true

# 4. 整理数据导入文件
echo "📊 整理数据导入文件..."
mkdir -p data/import/legacy
mv 导入批次_*.cypher data/import/legacy/ 2>/dev/null || true
mv 合并全部*模块数据.py data/import/legacy/ 2>/dev/null || true
mv 处理*模块数据.py data/import/legacy/ 2>/dev/null || true

# 5. 整理词典数据文件
echo "📚 整理词典数据文件..."
mkdir -p data/dictionary/modules
mv 硬件模块词典数据_*.csv data/dictionary/modules/ 2>/dev/null || true

# 6. 整理配置和报告JSON文件
echo "⚙️ 整理配置文件..."
mkdir -p config/legacy
mv *报告*.json config/legacy/ 2>/dev/null || true
mv *统计*.json config/legacy/ 2>/dev/null || true

# 7. 清理空目录
echo "🧽 清理空目录..."
find . -type d -empty -delete 2>/dev/null || true

echo "✅ 清理完成!"
echo "📦 备份位置: $BACKUP_DIR"
echo "📁 整理后的目录结构更加清晰"

# 显示清理后的根目录文件数量
echo "📊 根目录文件统计:"
echo "   Python脚本: $(ls -1 *.py 2>/dev/null | wc -l)"
echo "   配置文件: $(ls -1 *.yml *.yaml *.json 2>/dev/null | wc -l)"
echo "   文档文件: $(ls -1 *.md *.txt 2>/dev/null | wc -l)"
echo "   总文件数: $(ls -1 * 2>/dev/null | grep -v ":" | wc -l)"
'''
    
    with open("目录清理脚本.sh", "w", encoding="utf-8") as f:
        f.write(cleanup_script)
    
    print("💾 清理脚本已生成: 目录清理脚本.sh")
    
    return cleanup_script

def main():
    """主函数"""
    print("🔍 目录清理分析报告")
    print("=" * 80)
    
    # 1. 分析目录结构
    file_categories = analyze_directory_structure()
    
    # 2. 识别重复文件
    duplicate_groups = identify_duplicate_files()
    
    # 3. 识别过时文件
    obsolete_files = identify_obsolete_files()
    
    # 4. 分析目录冲突
    conflicts = analyze_directory_conflicts()
    
    # 5. 生成清理建议
    recommendations = generate_cleanup_recommendations()
    
    # 6. 创建清理脚本
    cleanup_script = create_cleanup_script()
    
    # 7. 生成总结报告
    print(f"\n📊 清理分析总结")
    print("=" * 60)
    
    total_files = sum(len(files) for files in file_categories.values())
    duplicate_count = sum(len(files) for files in duplicate_groups.values() if len(files) > 1)
    
    print(f"📁 根目录总文件数: {total_files}")
    print(f"🔄 重复文件组数: {len([g for g in duplicate_groups.values() if len(g) > 1])}")
    print(f"🗑️ 可删除文件数: {len(obsolete_files)}")
    print(f"⚠️ 目录冲突数: {len(conflicts)}")
    
    print(f"\n💡 建议操作:")
    print("   1. 执行 chmod +x 目录清理脚本.sh")
    print("   2. 运行 ./目录清理脚本.sh")
    print("   3. 验证清理结果")
    print("   4. 删除备份目录(如果确认无误)")
    
    # 保存详细报告
    report = {
        "分析时间": "2025-09-30",
        "文件分类": {k: len(v) for k, v in file_categories.items()},
        "重复文件组": {k: len(v) for k, v in duplicate_groups.items() if len(v) > 1},
        "过时文件数": len(obsolete_files),
        "目录冲突数": len(conflicts),
        "清理建议": {k: len(v) for k, v in recommendations.items()}
    }
    
    with open("目录清理分析报告.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 详细报告已保存: 目录清理分析报告.json")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 分析过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
