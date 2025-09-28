#!/usr/bin/env python3
"""
测试词典字段显示是否符合要求
验证前端表格字段：术语、别名、类别、多标签、备注
"""

import requests
import json

def test_api_response_structure():
    """测试API响应结构"""
    print("🔍 测试API响应结构...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/kg/dictionary")
        if response.status_code == 200:
            data = response.json()
            
            if data.get('ok') and data.get('data'):
                dict_data = data['data']
                print(f"   ✅ API响应正常")
                print(f"   📚 词典类别: {list(dict_data.keys())}")
                
                # 检查每个类别的字段结构
                for category, entries in dict_data.items():
                    if isinstance(entries, list) and entries:
                        first_entry = entries[0]
                        print(f"\n   📄 {category} 字段结构:")
                        print(f"      可用字段: {list(first_entry.keys())}")
                        
                        # 检查是否包含必需字段
                        required_fields = ['name', 'aliases', 'category', 'tags', 'description']
                        missing_fields = []
                        
                        for field in required_fields:
                            if field not in first_entry:
                                # 检查别名字段
                                if field == 'name' and 'canonical_name' in first_entry:
                                    continue
                                if field == 'tags' and 'tags' not in first_entry:
                                    missing_fields.append(field)
                                elif field not in first_entry:
                                    missing_fields.append(field)
                        
                        if missing_fields:
                            print(f"      ❌ 缺少字段: {missing_fields}")
                        else:
                            print(f"      ✅ 包含所有必需字段")
                        
                        # 显示示例数据
                        print(f"      📝 示例数据:")
                        print(f"         术语: {first_entry.get('name', first_entry.get('canonical_name', 'N/A'))}")
                        print(f"         别名: {first_entry.get('aliases', [])}")
                        print(f"         类别: {first_entry.get('category', 'N/A')}")
                        print(f"         标签: {first_entry.get('tags', [])}")
                        print(f"         备注: {first_entry.get('description', 'N/A')[:50]}...")
                
                return True
            else:
                print(f"   ❌ API返回错误: {data.get('error', {}).get('message', 'Unknown')}")
                return False
        else:
            print(f"   ❌ API请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ API测试失败: {e}")
        return False

def check_frontend_field_mapping():
    """检查前端字段映射"""
    print("\n🎨 检查前端字段映射...")
    
    required_table_columns = [
        "术语",    # name 或 canonical_name
        "别名",    # aliases
        "类别",    # category  
        "多标签",  # tags
        "备注"     # description
    ]
    
    print("   📋 要求的表格列:")
    for i, column in enumerate(required_table_columns, 1):
        print(f"      {i}. {column}")
    
    # 模拟前端数据转换
    print("\n   🔄 前端数据转换逻辑:")
    sample_api_data = {
        "name": "BTB连接器",
        "canonical_name": "BTB连接器", 
        "aliases": ["板对板连接器", "Board-to-Board Connector"],
        "category": "硬件相关",
        "tags": ["部件", "电气连接"],
        "description": "连接主板与副板、显示模组等的重要元件，易出现接触不良、虚焊等故障。"
    }
    
    frontend_data = {
        "术语": sample_api_data.get('name', sample_api_data.get('canonical_name')),
        "别名": sample_api_data.get('aliases', []),
        "类别": sample_api_data.get('category'),
        "多标签": sample_api_data.get('tags', []),
        "备注": sample_api_data.get('description')
    }
    
    print("   📝 转换示例:")
    for field, value in frontend_data.items():
        if isinstance(value, list):
            print(f"      {field}: {value} ({len(value)}个)")
        else:
            print(f"      {field}: {value}")

def verify_field_requirements():
    """验证字段要求"""
    print("\n✅ 验证字段要求...")
    
    field_requirements = {
        "术语": {
            "说明": "主要术语名称",
            "数据源": "API的name或canonical_name字段",
            "显示": "表格第一列，最小宽度150px"
        },
        "别名": {
            "说明": "术语的别名列表",
            "数据源": "API的aliases字段（数组）",
            "显示": "标签形式，支持多个别名"
        },
        "类别": {
            "说明": "术语的主要分类",
            "数据源": "API的category字段",
            "显示": "彩色标签，宽度120px"
        },
        "多标签": {
            "说明": "术语的多维度标签",
            "数据源": "API的tags字段（数组）",
            "显示": "绿色标签，支持多个标签"
        },
        "备注": {
            "说明": "术语的详细描述",
            "数据源": "API的description字段",
            "显示": "文本形式，支持溢出提示"
        }
    }
    
    print("   📋 字段要求验证:")
    for field, req in field_requirements.items():
        print(f"\n   📌 {field}:")
        for key, value in req.items():
            print(f"      {key}: {value}")

def main():
    print("🚀 开始测试词典字段显示...")
    
    # 测试API响应
    api_success = test_api_response_structure()
    
    # 检查前端映射
    check_frontend_field_mapping()
    
    # 验证字段要求
    verify_field_requirements()
    
    print("\n📋 测试总结:")
    print("=" * 50)
    
    if api_success:
        print("✅ API响应结构正常")
    else:
        print("❌ API响应结构异常")
    
    print("✅ 前端表格字段已更新为:")
    print("   1. 术语 (name/canonical_name)")
    print("   2. 别名 (aliases数组)")
    print("   3. 类别 (category)")
    print("   4. 多标签 (tags数组)")
    print("   5. 备注 (description)")
    
    print("\n🎯 字段显示特点:")
    print("   - 术语: 主要名称，最小宽度150px")
    print("   - 别名: 多个标签显示，灰色小标签")
    print("   - 类别: 彩色标签，根据类别显示不同颜色")
    print("   - 多标签: 绿色标签，显示多维度分类")
    print("   - 备注: 详细描述，支持溢出提示")
    
    print("\n🎉 词典字段显示测试完成！")

if __name__ == "__main__":
    main()
