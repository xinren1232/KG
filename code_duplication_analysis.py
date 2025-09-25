#!/usr/bin/env python3
"""
代码重复度分析工具
"""
import os
import hashlib
from pathlib import Path
from collections import defaultdict
import re

def get_file_hash(file_path):
    """计算文件内容的哈希值"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 去除空白行和注释进行比较
            lines = [line.strip() for line in content.split('\n') 
                    if line.strip() and not line.strip().startswith('#')]
            normalized_content = '\n'.join(lines)
            return hashlib.md5(normalized_content.encode()).hexdigest()
    except:
        return None

def analyze_function_similarity(file_path):
    """分析文件中的函数相似度"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取函数定义
        functions = re.findall(r'def\s+(\w+)\s*\([^)]*\):[^}]*?(?=\ndef|\nclass|\n@|\Z)', 
                              content, re.MULTILINE | re.DOTALL)
        return functions
    except:
        return []

def find_duplicate_files():
    """查找重复文件"""
    print("🔍 分析代码重复度...")
    print("=" * 60)
    
    file_hashes = defaultdict(list)
    api_files = []
    test_files = []
    config_files = []
    
    # 扫描项目文件
    for root, dirs, files in os.walk('.'):
        # 跳过特定目录
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv']]
        
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.vue', '.yaml', '.yml', '.json')):
                file_path = Path(root) / file
                
                # 分类文件
                if 'api' in str(file_path) or 'main' in file:
                    api_files.append(file_path)
                elif 'test' in file:
                    test_files.append(file_path)
                elif file.endswith(('.yaml', '.yml', '.json', '.env')):
                    config_files.append(file_path)
                
                # 计算哈希
                file_hash = get_file_hash(file_path)
                if file_hash:
                    file_hashes[file_hash].append(file_path)
    
    # 分析结果
    print("📊 文件统计:")
    print(f"   API文件: {len(api_files)}")
    print(f"   测试文件: {len(test_files)}")
    print(f"   配置文件: {len(config_files)}")
    
    # 查找完全重复的文件
    print("\n🚨 完全重复的文件:")
    duplicate_count = 0
    for file_hash, files in file_hashes.items():
        if len(files) > 1:
            duplicate_count += len(files) - 1
            print(f"   重复组 {len(files)} 个文件:")
            for file_path in files:
                print(f"     - {file_path}")
    
    if duplicate_count == 0:
        print("   ✅ 未发现完全重复的文件")
    else:
        print(f"   ❌ 发现 {duplicate_count} 个重复文件")
    
    return api_files, test_files, config_files

def analyze_api_duplication(api_files):
    """分析API文件的重复度"""
    print("\n🔍 API文件重复度分析:")
    print("-" * 40)
    
    # 分析API路由重复
    route_patterns = defaultdict(list)
    function_patterns = defaultdict(list)
    
    for file_path in api_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取路由定义
            routes = re.findall(r'@app\.(get|post|put|delete)\("([^"]+)"', content)
            for method, path in routes:
                route_key = f"{method.upper()} {path}"
                route_patterns[route_key].append(file_path)
            
            # 提取函数名
            functions = re.findall(r'def\s+(\w+)\s*\(', content)
            for func in functions:
                function_patterns[func].append(file_path)
                
        except Exception as e:
            print(f"   ❌ 分析 {file_path} 失败: {e}")
    
    # 报告路由重复
    print("📍 重复的API路由:")
    route_duplicates = 0
    for route, files in route_patterns.items():
        if len(files) > 1:
            route_duplicates += 1
            print(f"   {route}:")
            for file_path in files:
                print(f"     - {file_path}")
    
    if route_duplicates == 0:
        print("   ✅ 未发现重复的API路由")
    else:
        print(f"   ❌ 发现 {route_duplicates} 个重复路由")
    
    # 报告函数重复
    print("\n🔧 重复的函数名:")
    function_duplicates = 0
    common_functions = ['health_check', 'root', 'get_products', 'upload_document']
    
    for func, files in function_patterns.items():
        if len(files) > 1 and func in common_functions:
            function_duplicates += 1
            print(f"   {func}():")
            for file_path in files:
                print(f"     - {file_path}")
    
    if function_duplicates == 0:
        print("   ✅ 未发现重复的核心函数")
    else:
        print(f"   ❌ 发现 {function_duplicates} 个重复函数")

def analyze_config_duplication(config_files):
    """分析配置文件重复度"""
    print("\n⚙️ 配置文件重复度分析:")
    print("-" * 40)
    
    requirements_files = [f for f in config_files if 'requirements' in str(f)]
    yaml_files = [f for f in config_files if f.suffix in ['.yaml', '.yml']]
    
    print(f"📋 Requirements文件: {len(requirements_files)}")
    for req_file in requirements_files:
        print(f"   - {req_file}")
    
    print(f"📋 YAML配置文件: {len(yaml_files)}")
    for yaml_file in yaml_files:
        print(f"   - {yaml_file}")
    
    # 分析requirements重复
    if len(requirements_files) > 1:
        print("\n❌ 发现多个requirements文件，可能存在依赖冲突")
    else:
        print("\n✅ Requirements文件配置正常")

def generate_cleanup_recommendations():
    """生成清理建议"""
    print("\n" + "=" * 60)
    print("🎯 代码清理建议")
    print("=" * 60)
    
    recommendations = [
        {
            "priority": "🔥 高优先级",
            "items": [
                "删除重复的API服务文件 (保留 api/main_v01.py)",
                "合并重复的requirements.txt文件",
                "删除未使用的启动脚本",
                "清理重复的测试文件"
            ]
        },
        {
            "priority": "⚡ 中优先级", 
            "items": [
                "统一数据模型定义 (使用Pydantic v2)",
                "重构重复的函数逻辑",
                "整理配置文件结构",
                "优化目录组织"
            ]
        },
        {
            "priority": "💡 低优先级",
            "items": [
                "添加代码复用检查工具",
                "建立代码规范文档",
                "实现自动化重复检测",
                "优化导入结构"
            ]
        }
    ]
    
    for rec in recommendations:
        print(f"\n{rec['priority']}:")
        for item in rec['items']:
            print(f"   • {item}")

def main():
    """主函数"""
    print("🚀 代码重复度分析报告")
    print("=" * 60)
    
    # 分析文件重复
    api_files, test_files, config_files = find_duplicate_files()
    
    # 分析API重复
    analyze_api_duplication(api_files)
    
    # 分析配置重复
    analyze_config_duplication(config_files)
    
    # 生成建议
    generate_cleanup_recommendations()
    
    print("\n" + "=" * 60)
    print("📊 分析完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
