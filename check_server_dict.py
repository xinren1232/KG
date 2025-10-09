#!/usr/bin/env python3
import json

# 检查服务器词典文件
dict_file = "/opt/knowledge-graph/api/data/dictionary.json"
with open(dict_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"词典条目数: {len(data)}")

# 检查最后几条
print("\n最后5条:")
for i, entry in enumerate(data[-5:], len(data)-4):
    print(f"{i}. {entry['term']} - {entry['category']}")

