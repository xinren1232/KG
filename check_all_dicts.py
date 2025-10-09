#!/usr/bin/env python3
import json

files = [
    "/opt/knowledge-graph/api/data/dictionary.json",
    "/opt/knowledge-graph/apps/web/src/data/dictionary.json",
    "/opt/knowledge-graph/data/vocab/dictionary.json"
]

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"\n{file_path}")
        print(f"  条目数: {len(data)}")
        if len(data) > 0:
            print(f"  最后一条: {data[-1].get('term', 'N/A')}")
    except Exception as e:
        print(f"\n{file_path}")
        print(f"  错误: {e}")

