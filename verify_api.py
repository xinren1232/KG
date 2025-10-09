#!/usr/bin/env python3
import requests

# 测试API
url = "http://localhost:8000/kg/dictionary/entries?page_size=10000"
response = requests.get(url)
data = response.json()

print(f"API响应成功: {data.get('success')}")
print(f"返回总数: {data.get('data', {}).get('total')}")
print(f"实际条目数: {len(data.get('data', {}).get('entries', []))}")

