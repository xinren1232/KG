#!/usr/bin/env python3
import requests
import json

url = "http://localhost:8000/kg/graph?show_all=true&limit=1000"
response = requests.get(url)
data = response.json()

stats = data.get('data', {}).get('stats', {})

print("=" * 60)
print("图谱API统计:")
print("=" * 60)
print(f"  totalNodes: {stats.get('totalNodes')}")
print(f"  totalTerms: {stats.get('totalTerms')}")
print(f"  totalCategories: {stats.get('totalCategories')}")
print(f"  totalTags: {stats.get('totalTags')}")
print(f"  totalRelations: {stats.get('totalRelations')}")
print("=" * 60)

