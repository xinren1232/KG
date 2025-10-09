import json

with open('api/data/dictionary.json', encoding='utf-8') as f:
    data = json.load(f)

print(f"本地词典: {len(data)}条")
print(f"最后一条: {data[-1]['term']}")

