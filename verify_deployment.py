#!/usr/bin/env python3
"""
验证服务器部署结果
"""
import json

# 检查词典文件
print("=" * 80)
print("📊 服务器部署验证")
print("=" * 80)

dict_file = "/opt/knowledge-graph/api/data/dictionary.json"
with open(dict_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"\n✅ 词典总数: {len(data)}条")

# 分类统计
from collections import Counter
categories = Counter(e['category'] for e in data)
print(f"\n📂 分类分布:")
for cat, count in categories.most_common():
    print(f"   {cat}: {count}条")

# 检查新增术语
new_terms = [
    "白平衡偏移", "CMOS图像传感器", "光学暗箱", "AF成功率测试",
    "VCM对焦马达", "OIS模组", "ToF模组", "触控漂移", "屏闪严重"
]

print(f"\n🔍 新增术语检查:")
existing_terms = set(e['term'] for e in data)
for term in new_terms:
    status = "✅" if term in existing_terms else "❌"
    print(f"   {status} {term}")

print(f"\n" + "=" * 80)
print("✅ 验证完成")
print("=" * 80)
