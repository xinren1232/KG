#!/usr/bin/env python3
import json

# 检查API服务读取的词典文件
dict_file = "/opt/knowledge-graph/api/data/dictionary.json"
with open(dict_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"API词典文件条目数: {len(data)}")
print(f"\n最后5条:")
for i, entry in enumerate(data[-5:], len(data)-4):
    print(f"{i}. {entry['term']} - {entry['category']}")

