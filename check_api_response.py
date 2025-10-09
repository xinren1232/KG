#!/usr/bin/env python3
import requests
import json

# 检查API返回的数据结构
url = "http://localhost:8000/kg/graph?show_all=true&limit=1000"
response = requests.get(url)
data = response.json()

print("=" * 60)
print("API返回的完整数据结构:")
print("=" * 60)
print(json.dumps(data, indent=2, ensure_ascii=False))

print("\n" + "=" * 60)
print("数据字段分析:")
print("=" * 60)

if 'data' in data:
    print(f"✅ 有 'data' 字段")
    print(f"   data的键: {list(data['data'].keys())}")
    
    if 'stats' in data['data']:
        print(f"✅ 有 'stats' 字段")
        print(f"   stats内容: {json.dumps(data['data']['stats'], indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ 没有 'stats' 字段")
else:
    print(f"❌ 没有 'data' 字段")
    print(f"   顶层键: {list(data.keys())}")

