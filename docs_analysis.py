#!/usr/bin/env python3
"""
文档文件分析和整理工具
"""
import os
import re
from pathlib import Path
from datetime import datetime

def analyze_documentation():
    """分析所有文档文件"""
    print("📄 文档文件详细分析")
    print("=" * 60)
    
    doc_files = []
    
    # 查找所有文档文件
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv']]
        
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                doc_files.append(file_path)
    
    return doc_files

def categorize_docs(doc_files):
    """分类文档文件"""
    categories = {
        'user_docs': [],           # 用户文档
        'technical_docs': [],      # 技术文档
        'progress_reports': [],    # 进展报告
        'completion_reports': [],  # 完成报告
        'fix_reports': [],         # 修复报告
        'optimization_reports': [], # 优化报告
        'design_docs': [],         # 设计文档
        'implementation_docs': [], # 实现文档
        'summary_docs': [],        # 总结文档
        'outdated_docs': [],       # 过时文档
        'duplicate_docs': [],      # 重复文档
        'other_docs': []           # 其他文档
    }
    
    for doc_file in doc_files:
        file_name = doc_file.name.lower()
        
        # 用户文档
        if any(keyword in file_name for keyword in ['readme', '用户', 'user', 'manual', '手册']):
            categories['user_docs'].append(doc_file)
        # 技术文档
        elif any(keyword in file_name for keyword in ['technical', 'schema', 'ontology', 'api']):
            categories['technical_docs'].append(doc_file)
        # 进展报告
        elif any(keyword in file_name for keyword in ['progress', '进展', 'status']):
            categories['progress_reports'].append(doc_file)
        # 完成报告
        elif any(keyword in file_name for keyword in ['complete', '完成', 'final', 'summary']):
            categories['completion_reports'].append(doc_file)
        # 修复报告
        elif any(keyword in file_name for keyword in ['fix', 'repair', 'resolution', 'error']):
            categories['fix_reports'].append(doc_file)
        # 优化报告
        elif any(keyword in file_name for keyword in ['optimization', 'enhance', 'improve']):
            categories['optimization_reports'].append(doc_file)
        # 设计文档
        elif any(keyword in file_name for keyword in ['design', 'plan', 'architecture']):
            categories['design_docs'].append(doc_file)
        # 实现文档
        elif any(keyword in file_name for keyword in ['implementation', 'integration', 'parsing']):
            categories['implementation_docs'].append(doc_file)
        # 总结文档
        elif any(keyword in file_name for keyword in ['summary', '总结', 'achievement']):
            categories['summary_docs'].append(doc_file)
        # 过时文档 (包含日期)
        elif re.search(r'\d{4}|\d{2}_\d{2}|v\d+|old|backup', file_name):
            categories['outdated_docs'].append(doc_file)
        else:
            categories['other_docs'].append(doc_file)
    
    return categories

def analyze_doc_content(file_path):
    """分析文档内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # 检查文档质量
        has_title = content.startswith('#')
        has_structure = content.count('#') > 1
        has_content = len(non_empty_lines) > 10
        
        # 检查最后修改时间
        mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        days_old = (datetime.now() - mod_time).days
        
        return {
            'total_lines': len(lines),
            'content_lines': len(non_empty_lines),
            'has_title': has_title,
            'has_structure': has_structure,
            'has_content': has_content,
            'days_old': days_old,
            'size_kb': file_path.stat().st_size / 1024
        }
    except Exception as e:
        return {
            'total_lines': 0,
            'content_lines': 0,
            'has_title': False,
            'has_structure': False,
            'has_content': False,
            'days_old': 0,
            'size_kb': 0,
            'error': str(e)
        }

def print_doc_analysis(categories):
    """打印文档分析结果"""
    print("\n📊 文档分类结果:")
    print("-" * 40)
    
    for category, files in categories.items():
        if files:
            category_name = category.replace('_', ' ').title()
            print(f"\n{category_name} ({len(files)} 个):")
            for file_path in sorted(files):
                info = analyze_doc_content(file_path)
                quality = "🟢" if info['has_content'] and info['has_structure'] else "🟡" if info['has_content'] else "🔴"
                age = f"{info['days_old']}天前" if info['days_old'] > 0 else "今天"
                print(f"   {quality} {file_path} ({info['content_lines']} 行, {age})")

def generate_docs_cleanup_plan(categories):
    """生成文档清理计划"""
    print(f"\n" + "=" * 60)
    print("📄 文档整理计划")
    print("=" * 60)
    
    # 需要保留的核心文档
    keep_docs = []
    keep_docs.extend(categories['user_docs'])
    keep_docs.extend(categories['technical_docs'])
    keep_docs.extend(categories['design_docs'])
    
    # 需要合并的报告文档
    merge_docs = []
    merge_docs.extend(categories['progress_reports'])
    merge_docs.extend(categories['completion_reports'])
    merge_docs.extend(categories['fix_reports'])
    merge_docs.extend(categories['optimization_reports'])
    
    # 需要删除的过时文档
    delete_docs = []
    delete_docs.extend(categories['outdated_docs'])
    
    # 需要归档的实现文档
    archive_docs = []
    archive_docs.extend(categories['implementation_docs'])
    archive_docs.extend(categories['summary_docs'])
    
    print(f"✅ 保留核心文档 ({len(keep_docs)} 个):")
    for doc in sorted(keep_docs):
        print(f"   ✅ {doc}")
    
    print(f"\n🔄 合并报告文档 ({len(merge_docs)} 个):")
    for doc in sorted(merge_docs):
        print(f"   🔄 {doc}")
    
    print(f"\n🗑️ 删除过时文档 ({len(delete_docs)} 个):")
    for doc in sorted(delete_docs):
        print(f"   ❌ {doc}")
    
    print(f"\n📁 归档实现文档 ({len(archive_docs)} 个):")
    for doc in sorted(archive_docs):
        print(f"   📁 {doc}")
    
    # 建议的文档结构
    print(f"\n📂 建议的文档目录结构:")
    print("   docs/")
    print("   ├── README.md                    # 项目概述")
    print("   ├── user-guide.md               # 用户手册")
    print("   ├── api-documentation.md        # API文档")
    print("   ├── technical/")
    print("   │   ├── architecture.md         # 系统架构")
    print("   │   ├── database-schema.md      # 数据库设计")
    print("   │   └── deployment.md           # 部署指南")
    print("   ├── development/")
    print("   │   ├── setup.md                # 开发环境")
    print("   │   ├── contributing.md         # 贡献指南")
    print("   │   └── testing.md              # 测试指南")
    print("   └── archive/")
    print("       ├── project-reports/        # 项目报告归档")
    print("       └── implementation-logs/    # 实现记录归档")
    
    return keep_docs, merge_docs, delete_docs, archive_docs

def main():
    """主函数"""
    doc_files = analyze_documentation()
    print(f"发现 {len(doc_files)} 个文档文件")
    
    categories = categorize_docs(doc_files)
    print_doc_analysis(categories)
    
    keep_docs, merge_docs, delete_docs, archive_docs = generate_docs_cleanup_plan(categories)
    
    print(f"\n" + "=" * 60)
    print("📋 文档分析完成")
    print(f"总计: {len(doc_files)} 个文档")
    print(f"保留核心: {len(keep_docs)} 个")
    print(f"合并报告: {len(merge_docs)} 个")
    print(f"删除过时: {len(delete_docs)} 个")
    print(f"归档实现: {len(archive_docs)} 个")
    print("=" * 60)
    
    return categories, keep_docs, merge_docs, delete_docs, archive_docs

if __name__ == "__main__":
    main()
