#!/usr/bin/env python3
"""
测试文件详细分析和分类工具
"""
import os
import re
from pathlib import Path
from datetime import datetime

def analyze_test_files():
    """分析所有测试文件"""
    print("🧪 测试文件详细分析")
    print("=" * 60)
    
    test_files = []
    
    # 查找所有测试文件
    test_patterns = [
        r'test_.*\.py$',
        r'.*_test\.py$', 
        r'test.*\.html$',
        r'check_.*\.py$',
        r'.*_verification.*\.py$',
        r'.*_function_test\.py$'
    ]
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv']]
        
        for file in files:
            file_path = Path(root) / file
            
            # 检查是否是测试文件
            for pattern in test_patterns:
                if re.search(pattern, str(file_path), re.IGNORECASE):
                    test_files.append(file_path)
                    break
    
    return test_files

def categorize_test_files(test_files):
    """分类测试文件"""
    categories = {
        'api_tests': [],           # API测试
        'frontend_tests': [],      # 前端测试
        'parsing_tests': [],       # 解析测试
        'dictionary_tests': [],    # 词典测试
        'integration_tests': [],   # 集成测试
        'system_tests': [],        # 系统测试
        'verification_tests': [],  # 验证测试
        'optimization_tests': [],  # 优化测试
        'debug_tests': [],         # 调试测试
        'outdated_tests': [],      # 过时测试
        'duplicate_tests': [],     # 重复测试
        'other_tests': []          # 其他测试
    }
    
    for test_file in test_files:
        file_name = test_file.name.lower()
        file_str = str(test_file).lower()
        
        # API测试
        if any(keyword in file_name for keyword in ['api', 'endpoint']):
            categories['api_tests'].append(test_file)
        # 前端测试
        elif any(keyword in file_name for keyword in ['frontend', 'vue', 'ui', 'navigation']):
            categories['frontend_tests'].append(test_file)
        # 解析测试
        elif any(keyword in file_name for keyword in ['parsing', 'parse', 'docx', 'excel', 'pdf']):
            categories['parsing_tests'].append(test_file)
        # 词典测试
        elif any(keyword in file_name for keyword in ['dictionary', 'dict']):
            categories['dictionary_tests'].append(test_file)
        # 集成测试
        elif any(keyword in file_name for keyword in ['integration', 'end_to_end', 'e2e']):
            categories['integration_tests'].append(test_file)
        # 系统测试
        elif any(keyword in file_name for keyword in ['system', 'final', 'complete']):
            categories['system_tests'].append(test_file)
        # 验证测试
        elif any(keyword in file_name for keyword in ['verification', 'check', 'status']):
            categories['verification_tests'].append(test_file)
        # 优化测试
        elif any(keyword in file_name for keyword in ['optimization', 'optimized', 'enhanced']):
            categories['optimization_tests'].append(test_file)
        # 调试测试
        elif any(keyword in file_name for keyword in ['debug', 'fix', 'async']):
            categories['debug_tests'].append(test_file)
        # 过时测试 (包含日期或版本号)
        elif re.search(r'\d{4}|\d{2}_\d{2}|v\d+|old|backup', file_name):
            categories['outdated_tests'].append(test_file)
        else:
            categories['other_tests'].append(test_file)
    
    # 检查重复测试
    file_names = [f.name for f in test_files]
    for test_file in test_files:
        base_name = test_file.stem
        similar_files = [f for f in test_files if f.stem.startswith(base_name) and f != test_file]
        if similar_files and test_file not in categories['duplicate_tests']:
            categories['duplicate_tests'].append(test_file)
    
    return categories

def analyze_file_content(file_path):
    """分析文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计信息
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # 检查是否有实际测试代码
        has_tests = any(keyword in content.lower() for keyword in [
            'def test_', 'class test', 'assert', 'unittest', 'pytest'
        ])
        
        # 检查是否是HTML文件
        is_html = file_path.suffix.lower() == '.html'
        
        # 检查最后修改时间
        mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        days_old = (datetime.now() - mod_time).days
        
        return {
            'total_lines': len(lines),
            'code_lines': len(non_empty_lines),
            'has_tests': has_tests,
            'is_html': is_html,
            'days_old': days_old,
            'size_kb': file_path.stat().st_size / 1024
        }
    except Exception as e:
        return {
            'total_lines': 0,
            'code_lines': 0,
            'has_tests': False,
            'is_html': False,
            'days_old': 0,
            'size_kb': 0,
            'error': str(e)
        }

def print_categorization_results(categories):
    """打印分类结果"""
    print("\n📊 测试文件分类结果:")
    print("-" * 40)
    
    for category, files in categories.items():
        if files:
            category_name = category.replace('_', ' ').title()
            print(f"\n{category_name} ({len(files)} 个):")
            for file_path in sorted(files):
                info = analyze_file_content(file_path)
                status = "🟢" if info['has_tests'] else "🔴"
                age = f"{info['days_old']}天前" if info['days_old'] > 0 else "今天"
                print(f"   {status} {file_path} ({info['code_lines']} 行, {age})")

def generate_cleanup_plan(categories):
    """生成清理计划"""
    print(f"\n" + "=" * 60)
    print("🗑️ 测试文件清理计划")
    print("=" * 60)
    
    # 立即删除的文件
    to_delete = []
    to_delete.extend(categories['debug_tests'])
    to_delete.extend(categories['outdated_tests'])
    
    # 需要合并的重复文件
    to_merge = categories['duplicate_tests']
    
    # 需要重组的文件
    to_reorganize = []
    to_reorganize.extend(categories['api_tests'])
    to_reorganize.extend(categories['frontend_tests'])
    to_reorganize.extend(categories['parsing_tests'])
    to_reorganize.extend(categories['integration_tests'])
    
    print(f"🔥 立即删除 ({len(to_delete)} 个):")
    for file_path in sorted(to_delete):
        print(f"   ❌ {file_path}")
    
    print(f"\n🔄 需要合并 ({len(to_merge)} 个):")
    for file_path in sorted(to_merge):
        print(f"   🔄 {file_path}")
    
    print(f"\n📁 需要重组 ({len(to_reorganize)} 个):")
    for file_path in sorted(to_reorganize):
        print(f"   📁 {file_path}")
    
    # 建议的新目录结构
    print(f"\n📂 建议的测试目录结构:")
    print("   tests/")
    print("   ├── unit/")
    print("   │   ├── test_api.py")
    print("   │   ├── test_parsing.py")
    print("   │   └── test_dictionary.py")
    print("   ├── integration/")
    print("   │   ├── test_api_integration.py")
    print("   │   └── test_frontend_integration.py")
    print("   ├── e2e/")
    print("   │   ├── test_system_workflow.py")
    print("   │   └── test_user_scenarios.py")
    print("   └── fixtures/")
    print("       ├── test_data.json")
    print("       └── sample_files/")
    
    return to_delete, to_merge, to_reorganize

def main():
    """主函数"""
    test_files = analyze_test_files()
    print(f"发现 {len(test_files)} 个测试文件")
    
    categories = categorize_test_files(test_files)
    print_categorization_results(categories)
    
    to_delete, to_merge, to_reorganize = generate_cleanup_plan(categories)
    
    print(f"\n" + "=" * 60)
    print("📋 测试文件分析完成")
    print(f"总计: {len(test_files)} 个文件")
    print(f"建议删除: {len(to_delete)} 个")
    print(f"建议合并: {len(to_merge)} 个")
    print(f"建议重组: {len(to_reorganize)} 个")
    print("=" * 60)
    
    return categories, to_delete, to_merge, to_reorganize

if __name__ == "__main__":
    main()
