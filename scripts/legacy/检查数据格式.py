#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查dictionary.json数据格式
"""

import json
from collections import Counter

def check_data():
    """检查数据格式"""
    print("🔍 检查dictionary.json数据格式")
    print("=" * 50)
    
    try:
        # 读取数据
        with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 总条数: {len(data)}")
        
        # 检查数据结构
        if data:
            sample = data[0]
            print(f"📋 数据字段: {list(sample.keys())}")
            print(f"📋 示例数据: {sample}")
        
        # 统计分类
        categories = [item.get('category', '') for item in data]
        category_counts = Counter(categories)
        
        print(f"\n📊 分类统计:")
        for category, count in category_counts.most_common():
            print(f"  {category}: {count} 条")
        
        # 检查空值
        empty_terms = [item for item in data if not item.get('term', '').strip()]
        empty_categories = [item for item in data if not item.get('category', '').strip()]
        
        print(f"\n🔍 数据质量:")
        print(f"  空term: {len(empty_terms)} 条")
        print(f"  空category: {len(empty_categories)} 条")
        
        # 检查我们期望的8个分类
        expected_categories = {'Symptom', 'Component', 'Tool', 'Process', 'TestCase', 'Metric', 'Material', 'Role'}
        actual_categories = set(categories)
        
        print(f"\n📊 分类对比:")
        print(f"  期望分类: {expected_categories}")
        print(f"  实际分类: {actual_categories}")
        print(f"  匹配的分类: {expected_categories & actual_categories}")
        print(f"  缺失的分类: {expected_categories - actual_categories}")
        print(f"  多余的分类: {actual_categories - expected_categories}")
        
        return data, category_counts
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return None, None

def main():
    data, category_counts = check_data()
    
    if data:
        print(f"\n" + "=" * 50)
        print(f"📊 总结")
        print(f"=" * 50)
        print(f"✅ 数据文件读取成功")
        print(f"📊 总条数: {len(data)}")
        print(f"📊 分类数: {len(category_counts)}")
        
        # 检查是否需要重新导入
        if len(data) == 1124:
            print(f"✅ 数据条数正确")
        else:
            print(f"⚠️ 数据条数异常，期望1124，实际{len(data)}")

if __name__ == "__main__":
    main()
