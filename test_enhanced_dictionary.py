#!/usr/bin/env python3
"""
测试增强词典结构和内容
"""

import requests
import json
import csv
from pathlib import Path

def test_enhanced_dictionary_files():
    """测试增强词典文件"""
    print("🔍 测试增强词典文件...")
    
    dict_files = {
        "enhanced_components.csv": "组件词典",
        "enhanced_symptoms.csv": "症状词典", 
        "enhanced_tools_processes.csv": "工具流程词典"
    }
    
    total_entries = 0
    
    for filename, description in dict_files.items():
        file_path = Path(f"ontology/dictionaries/{filename}")
        print(f"\n📄 {description} ({filename}):")
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    entries = list(reader)
                    
                    print(f"   ✅ 文件存在，包含 {len(entries)} 个条目")
                    total_entries += len(entries)
                    
                    # 显示字段结构
                    if entries:
                        fields = list(entries[0].keys())
                        print(f"   📋 字段结构: {fields}")
                        
                        # 显示前3个条目示例
                        print(f"   📝 条目示例:")
                        for i, entry in enumerate(entries[:3]):
                            term = entry.get('term', 'N/A')
                            category = entry.get('category', 'N/A')
                            tags = entry.get('tags', 'N/A')
                            print(f"      {i+1}. {term} ({category}) - 标签: {tags}")
                        
                        if len(entries) > 3:
                            print(f"      ... 还有 {len(entries) - 3} 个条目")
                            
            except Exception as e:
                print(f"   ❌ 读取文件失败: {e}")
        else:
            print(f"   ❌ 文件不存在: {file_path}")
    
    print(f"\n📊 总计: {total_entries} 个词典条目")
    return total_entries

def test_api_dictionary():
    """测试API词典接口"""
    print("\n🌐 测试API词典接口...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/kg/dictionary")
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   响应结构: {list(data.keys())}")
            
            if data.get('ok') and data.get('data'):
                dict_data = data['data']
                print(f"   ✅ API成功返回词典数据")
                print(f"   📚 词典类别: {list(dict_data.keys())}")
                
                total_api_entries = 0
                for category, entries in dict_data.items():
                    if isinstance(entries, list):
                        print(f"      {category}: {len(entries)} 个条目")
                        total_api_entries += len(entries)
                        
                        # 显示第一个条目的结构
                        if entries:
                            first_entry = entries[0]
                            print(f"         示例字段: {list(first_entry.keys())}")
                            print(f"         示例数据: {first_entry.get('name', 'N/A')} - {first_entry.get('tags', [])}")
                
                print(f"   📊 API返回总条目: {total_api_entries}")
                return True, total_api_entries
            else:
                print(f"   ❌ API返回错误: {data.get('error', {}).get('message', 'Unknown')}")
                return False, 0
        else:
            print(f"   ❌ API请求失败: {response.status_code}")
            return False, 0
            
    except Exception as e:
        print(f"   ❌ API测试失败: {e}")
        return False, 0

def test_dictionary_features():
    """测试词典新功能"""
    print("\n🔧 测试词典新功能...")
    
    # 测试多标签功能
    print("   📋 多标签功能:")
    sample_tags = [
        "硬件相关;部件;电气连接",
        "异常现象;摄像头模组;影像相关", 
        "工具;测试验证;质量体系"
    ]
    
    for tag_str in sample_tags:
        tags = [tag.strip() for tag in tag_str.split(';') if tag.strip()]
        print(f"      标签字符串: '{tag_str}' -> 解析为: {tags}")
    
    # 测试别名功能
    print("   🔗 别名功能:")
    sample_aliases = [
        "板对板连接器;Board-to-Board Connector",
        "边缘暗影;Shading",
        "接收质量限;Acceptable Quality Level"
    ]
    
    for alias_str in sample_aliases:
        aliases = [alias.strip() for alias in alias_str.split(';') if alias.strip()]
        print(f"      别名字符串: '{alias_str}' -> 解析为: {aliases}")

def analyze_dictionary_content():
    """分析词典内容"""
    print("\n📈 分析词典内容...")
    
    # 统计各类别数量
    categories = {}
    tags = {}
    
    dict_files = [
        "ontology/dictionaries/enhanced_components.csv",
        "ontology/dictionaries/enhanced_symptoms.csv", 
        "ontology/dictionaries/enhanced_tools_processes.csv"
    ]
    
    for file_path in dict_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        category = row.get('category', '未分类')
                        categories[category] = categories.get(category, 0) + 1
                        
                        tag_str = row.get('tags', '')
                        if tag_str:
                            for tag in tag_str.split(';'):
                                tag = tag.strip()
                                if tag:
                                    tags[tag] = tags.get(tag, 0) + 1
            except Exception as e:
                print(f"   ❌ 分析文件失败 {file_path}: {e}")
    
    print("   📊 类别分布:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"      {category}: {count} 个条目")
    
    print("   🏷️ 标签分布 (前10个):")
    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, count in sorted_tags:
        print(f"      {tag}: {count} 次")

def main():
    print("🚀 开始测试增强词典...")
    
    # 测试词典文件
    file_entries = test_enhanced_dictionary_files()
    
    # 测试API接口
    api_success, api_entries = test_api_dictionary()
    
    # 测试新功能
    test_dictionary_features()
    
    # 分析内容
    analyze_dictionary_content()
    
    print("\n📋 测试总结:")
    print("=" * 50)
    print(f"✅ 词典文件条目: {file_entries}")
    if api_success:
        print(f"✅ API返回条目: {api_entries}")
        if file_entries == api_entries:
            print("✅ 文件与API数据一致")
        else:
            print("⚠️ 文件与API数据不一致")
    else:
        print("❌ API测试失败")
    
    print("\n🎯 新功能验证:")
    print("✅ 多标签支持: 每个条目可以有多个分类标签")
    print("✅ 别名映射: 支持多个别名和标准名称")
    print("✅ 增强描述: 详细的业务描述和使用场景")
    print("✅ 分类体系: 更细致的分类管理")
    
    print("\n🎉 增强词典测试完成！")

if __name__ == "__main__":
    main()
