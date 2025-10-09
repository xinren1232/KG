#!/usr/bin/env python3
import requests
import json

# 测试API返回
url = "http://localhost:8000/kg/dictionary"
response = requests.get(url)
data = response.json()

print(f"API返回total: {data.get('total')}")
print(f"API返回message: {data.get('message')}")

# 统计各分类数量
if 'data' in data:
    total_items = 0
    for category, items in data['data'].items():
        count = len(items)
        total_items += count
        print(f"{category}: {count}条")
    print(f"\n实际条目总数: {total_items}")

