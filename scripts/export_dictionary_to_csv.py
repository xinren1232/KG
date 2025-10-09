#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出现有 api/data/dictionary.json 为标准化 CSV: data/dictionary/dictionary_v1.csv
列: term,aliases,category,tags,note,source,version
- aliases/tags 用分号分隔
- source 固定为 dictionary_v1
- version 使用今天日期 YYYY-MM-DD
"""
import json
import csv
from pathlib import Path
from datetime import date

DICT_PATH = Path('api/data/dictionary.json')
OUT_DIR = Path('data/dictionary')
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = OUT_DIR / 'dictionary_v1.csv'

def norm_list(v):
    if not v:
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return [str(v).strip()] if str(v).strip() else []

if __name__ == '__main__':
    assert DICT_PATH.exists(), f'词典文件不存在: {DICT_PATH}'
    data = json.load(open(DICT_PATH, 'r', encoding='utf-8'))
    if isinstance(data, dict) and 'entries' in data:
        data = data['entries']
    assert isinstance(data, list), '词典JSON格式应为数组'

    today = date.today().isoformat()

    rows = []
    for item in data:
        term = (item.get('term') or item.get('name') or '').strip()
        category = (item.get('category') or '').strip()
        aliases = norm_list(item.get('aliases'))
        tags = norm_list(item.get('tags'))
        note = (item.get('definition') or item.get('description') or '').strip()
        if not term or not category:
            continue
        rows.append({
            'term': term,
            'aliases': ';'.join(aliases),
            'category': category,
            'tags': ';'.join(sorted(set(tags))),
            'note': note,
            'source': 'dictionary_v1',
            'version': today,
        })

    # 去重：按 (term, category) 保留第一条
    seen = set()
    deduped = []
    for r in rows:
        key = (r['term'], r['category'])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(r)

    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['term','aliases','category','tags','note','source','version'])
        w.writeheader()
        w.writerows(deduped)

    print(f'导出完成: {OUT_CSV} 共 {len(deduped)} 条')
