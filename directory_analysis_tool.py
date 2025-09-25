#!/usr/bin/env python3
"""
目录结构深度分析工具
"""
import os
from pathlib import Path
from collections import defaultdict
import re

def analyze_directory_structure():
    """分析目录结构"""
    print("🔍 深度目录结构分析")
    print("=" * 60)
    
    # 统计信息
    stats = {
        'total_files': 0,
        'total_dirs': 0,
        'file_types': defaultdict(int),
        'large_dirs': [],
        'test_files': [],
        'doc_files': [],
        'temp_files': [],
        'config_files': []
    }
    
    # 需要特别关注的文件模式
    test_patterns = [r'test_.*\.py$', r'.*_test\.py$', r'.*\.test\..*$', r'test.*\.html$']
    doc_patterns = [r'.*_report\.md$', r'.*_summary\.md$', r'.*_complete.*\.md$', r'README.*', r'.*\.md$']
    temp_patterns = [r'debug_.*', r'temp_.*', r'tmp_.*', r'.*\.tmp$', r'.*\.log$', r'.*\.cache$']
    config_patterns = [r'.*\.env.*', r'.*\.yml$', r'.*\.yaml$', r'.*\.json$', r'requirements.*\.txt$']
    
    def categorize_file(file_path):
        """分类文件"""
        file_str = str(file_path)
        
        # 检查测试文件
        for pattern in test_patterns:
            if re.search(pattern, file_str, re.IGNORECASE):
                stats['test_files'].append(file_path)
                return 'test'
        
        # 检查文档文件
        for pattern in doc_patterns:
            if re.search(pattern, file_str, re.IGNORECASE):
                stats['doc_files'].append(file_path)
                return 'doc'
        
        # 检查临时文件
        for pattern in temp_patterns:
            if re.search(pattern, file_str, re.IGNORECASE):
                stats['temp_files'].append(file_path)
                return 'temp'
        
        # 检查配置文件
        for pattern in config_patterns:
            if re.search(pattern, file_str, re.IGNORECASE):
                stats['config_files'].append(file_path)
                return 'config'
        
        return 'other'
    
    # 遍历目录
    try:
        for root, dirs, files in os.walk('.'):
            # 跳过特定目录
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv']]

            root_path = Path(root)
            stats['total_dirs'] += 1

            # 统计大目录
            if len(files) > 10:
                stats['large_dirs'].append((root_path, len(files)))

            for file in files:
                try:
                    file_path = root_path / file
                    stats['total_files'] += 1

                    # 统计文件类型
                    suffix = file_path.suffix.lower()
                    stats['file_types'][suffix] += 1

                    # 分类文件
                    categorize_file(file_path)
                except Exception as e:
                    print(f"处理文件 {file} 时出错: {e}")
                    continue
    except Exception as e:
        print(f"遍历目录时出错: {e}")
    
    return stats

def print_analysis_results(stats):
    """打印分析结果"""
    print(f"📊 总体统计:")
    print(f"   总文件数: {stats['total_files']}")
    print(f"   总目录数: {stats['total_dirs']}")
    
    print(f"\n📁 文件类型分布:")
    sorted_types = sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)
    for ext, count in sorted_types[:10]:
        ext_name = ext if ext else '(无扩展名)'
        print(f"   {ext_name}: {count} 个")
    
    print(f"\n📂 大目录 (>10个文件):")
    for dir_path, file_count in sorted(stats['large_dirs'], key=lambda x: x[1], reverse=True):
        print(f"   {dir_path}: {file_count} 个文件")
    
    print(f"\n🧪 测试文件 ({len(stats['test_files'])} 个):")
    for test_file in sorted(stats['test_files'])[:15]:  # 显示前15个
        print(f"   {test_file}")
    if len(stats['test_files']) > 15:
        print(f"   ... 还有 {len(stats['test_files']) - 15} 个测试文件")
    
    print(f"\n📄 文档文件 ({len(stats['doc_files'])} 个):")
    for doc_file in sorted(stats['doc_files'])[:10]:  # 显示前10个
        print(f"   {doc_file}")
    if len(stats['doc_files']) > 10:
        print(f"   ... 还有 {len(stats['doc_files']) - 10} 个文档文件")
    
    print(f"\n🗑️ 临时文件 ({len(stats['temp_files'])} 个):")
    for temp_file in sorted(stats['temp_files']):
        print(f"   {temp_file}")
    
    print(f"\n⚙️ 配置文件 ({len(stats['config_files'])} 个):")
    for config_file in sorted(stats['config_files']):
        print(f"   {config_file}")

def generate_optimization_recommendations(stats):
    """生成优化建议"""
    print(f"\n" + "=" * 60)
    print("🎯 目录结构优化建议")
    print("=" * 60)
    
    # 测试文件优化
    if len(stats['test_files']) > 20:
        print(f"\n🧪 测试文件优化 (当前: {len(stats['test_files'])} 个)")
        print("   建议:")
        print("   • 创建 tests/ 目录")
        print("   • 按功能分类: tests/unit/, tests/integration/, tests/e2e/")
        print("   • 删除重复和过时的测试文件")
        print(f"   • 目标: 减少到 15-20 个有组织的测试文件")
    
    # 文档文件优化
    if len(stats['doc_files']) > 15:
        print(f"\n📄 文档文件优化 (当前: {len(stats['doc_files'])} 个)")
        print("   建议:")
        print("   • 创建 docs/ 目录")
        print("   • 合并相似的报告文档")
        print("   • 删除过时的进展报告")
        print("   • 保留: README.md, 用户手册, 技术文档")
    
    # 临时文件清理
    if len(stats['temp_files']) > 0:
        print(f"\n🗑️ 临时文件清理 (当前: {len(stats['temp_files'])} 个)")
        print("   建议: 立即删除所有临时文件")
    
    # 大目录优化
    if stats['large_dirs']:
        print(f"\n📂 大目录优化:")
        for dir_path, file_count in stats['large_dirs']:
            if file_count > 20:
                print(f"   {dir_path} ({file_count} 个文件) - 需要子目录分类")
    
    # 配置文件优化
    config_count = len(stats['config_files'])
    if config_count > 10:
        print(f"\n⚙️ 配置文件优化 (当前: {config_count} 个)")
        print("   建议:")
        print("   • 合并相似的配置文件")
        print("   • 删除未使用的配置")
        print("   • 统一配置格式")

def main():
    """主函数"""
    stats = analyze_directory_structure()
    print_analysis_results(stats)
    generate_optimization_recommendations(stats)
    
    print(f"\n" + "=" * 60)
    print("📋 分析完成")
    print("=" * 60)
    
    return stats

if __name__ == "__main__":
    main()
