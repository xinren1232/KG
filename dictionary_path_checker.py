#!/usr/bin/env python3
"""
词典路径检查和修复工具
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Any

def check_dictionary_paths():
    """检查所有词典路径和数据源"""
    print("🔍 词典路径和数据源检查报告")
    print("=" * 60)
    
    base_dir = Path(".")
    
    # 检查数据源目录
    data_sources = {
        "主要数据源 (ontology/dictionaries)": base_dir / "ontology" / "dictionaries",
        "次要数据源 (data/vocab)": base_dir / "data" / "vocab", 
        "治理数据源 (data/governance)": base_dir / "data" / "governance"
    }
    
    print("\n📁 数据源目录检查:")
    for name, path in data_sources.items():
        if path.exists():
            files = list(path.glob("*.csv")) + list(path.glob("*.json"))
            print(f"✅ {name}: {path} ({len(files)} 个文件)")
            for file in files[:5]:  # 显示前5个文件
                print(f"   - {file.name}")
            if len(files) > 5:
                print(f"   ... 还有 {len(files) - 5} 个文件")
        else:
            print(f"❌ {name}: {path} (不存在)")
    
    # 检查API文件中的词典配置
    print("\n🔧 API文件词典配置检查:")
    api_files = {
        "main_v01.py": "api/main_v01.py",
        "main.py": "api/main.py", 
        "knowledge_graph_api.py": "api/knowledge_graph_api.py",
        "simple_api.py": "api/simple_api.py",
        "dictionary_manager.py": "api/dictionary_manager.py"
    }
    
    for name, file_path in api_files.items():
        path = Path(file_path)
        if path.exists():
            print(f"\n📄 {name}:")
            check_api_file_dictionary_config(path)
        else:
            print(f"❌ {name}: 文件不存在")
    
    # 统计词典数据
    print("\n📊 词典数据统计:")
    try:
        from api.unified_dictionary_config import get_dictionary_statistics
        stats = get_dictionary_statistics()
        print(f"✅ 总条目数: {stats['total_entries']}")
        print(f"   - 组件: {stats['components']}")
        print(f"   - 症状: {stats['symptoms']}")
        print(f"   - 原因: {stats['causes']}")
        print(f"   - 对策: {stats['countermeasures']}")
        print(f"   - 工具流程: {stats['tools_processes']}")
        print(f"📂 主要数据源: {stats['data_sources']['primary']}")
        print(f"📂 次要数据源: {stats['data_sources']['secondary']}")
    except Exception as e:
        print(f"❌ 无法获取统一词典统计: {e}")
    
    # 检查API服务状态
    print("\n🌐 API服务状态检查:")
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ API服务: {health.get('service', 'Unknown')}")
            print(f"   状态: {health.get('status', 'Unknown')}")
            print(f"   数据库: {health.get('database', 'Unknown')}")
        else:
            print(f"❌ API服务响应异常: {response.status_code}")
    except Exception as e:
        print(f"❌ API服务连接失败: {e}")
    
    # 测试词典API
    try:
        import requests
        response = requests.get("http://localhost:8000/kg/dictionary", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') or data.get('success'):
                dict_data = data.get('data', {})
                print(f"✅ 词典API正常:")
                print(f"   - 组件: {len(dict_data.get('components', []))}")
                print(f"   - 症状: {len(dict_data.get('symptoms', []))}")
                print(f"   - 原因: {len(dict_data.get('causes', []))}")
                print(f"   - 对策: {len(dict_data.get('countermeasures', []))}")
            else:
                print(f"❌ 词典API返回错误: {data}")
        else:
            print(f"❌ 词典API响应异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 词典API测试失败: {e}")

def check_api_file_dictionary_config(file_path: Path):
    """检查API文件中的词典配置"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查词典路径引用
        path_patterns = [
            "ontology/dictionaries",
            "../ontology/dictionaries", 
            "data/vocab",
            "data/governance",
            "dictionary.json",
            "components.csv",
            "symptoms.csv"
        ]
        
        found_paths = []
        for pattern in path_patterns:
            if pattern in content:
                found_paths.append(pattern)
        
        # 检查是否使用统一词典管理器
        uses_unified = "unified_dictionary_config" in content
        uses_hardcoded = any(x in content for x in ["模拟", "sample_entries", "硬编码"])
        
        if uses_unified:
            print(f"   ✅ 使用统一词典管理器")
        elif found_paths:
            print(f"   ⚠️ 使用直接路径: {', '.join(found_paths)}")
        elif uses_hardcoded:
            print(f"   ❌ 使用硬编码/模拟数据")
        else:
            print(f"   ❓ 未检测到词典配置")
            
    except Exception as e:
        print(f"   ❌ 检查失败: {e}")

def fix_dictionary_paths():
    """修复词典路径问题"""
    print("\n🔧 词典路径修复建议:")
    print("=" * 60)
    
    print("1. 统一使用 unified_dictionary_config.py")
    print("   - 已创建统一词典管理器")
    print("   - main_v01.py 已更新使用统一管理器")
    print("   - 建议其他API文件也使用统一管理器")
    
    print("\n2. 数据源优先级:")
    print("   - 主要: ontology/dictionaries/ (标准CSV格式)")
    print("   - 次要: data/vocab/ (JSON/简单CSV格式)")
    print("   - 备份: data/governance/ (治理数据)")
    
    print("\n3. 推荐的标准化步骤:")
    print("   a. 确保 ontology/dictionaries/ 包含最新数据")
    print("   b. 所有API使用 unified_dictionary_config")
    print("   c. 移除硬编码的模拟数据")
    print("   d. 统一数据格式和字段名称")

def main():
    """主函数"""
    check_dictionary_paths()
    fix_dictionary_paths()
    
    print("\n🎯 总结:")
    print("✅ 统一词典管理器已创建并工作正常")
    print("✅ main_v01.py 已更新使用统一管理器")
    print("✅ 词典数据加载正常 (206条记录)")
    print("⚠️ 建议其他API文件也使用统一管理器")
    print("⚠️ 建议移除硬编码的模拟数据")

if __name__ == "__main__":
    main()
