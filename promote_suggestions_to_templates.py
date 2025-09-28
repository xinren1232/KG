#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 data/relations/suggestions/*.csv 中置信度 >= 阈值 的候选，合并到 data/relations/templates/*.csv
- 默认阈值 0.85，可调整 --min 0.8
- 自动去重（按 source_term + target_term 键）
用法：
  python promote_suggestions_to_templates.py --min 0.85
"""
import csv
from pathlib import Path
import argparse

SUG_DIR = Path('data/relations/suggestions')
TPL_DIR = Path('data/relations/templates')

FILES = [
    'testcases_measures_metrics.csv',
    'testcases_uses_tools.csv',
    'testcases_covers_components.csv',
    'process_uses_tools.csv',
    'process_consumes_materials.csv',
    'component_has_symptom.csv',
]

def read_rows(path: Path):
    rows = []
    if not path.exists():
        return rows
    with path.open('r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader((line for line in f if not line.lstrip().startswith('#')))
        for r in reader:
            rows.append(r)
    return rows


def write_rows(path: Path, rows, mode='w'):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open(mode, encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['source_term','target_term','confidence','source','note'])
        if mode == 'w':
            w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min', type=float, default=0.85, help='最低置信度阈值，默认0.85')
    args = ap.parse_args()

    for name in FILES:
        sug = SUG_DIR / name
        tpl = TPL_DIR / name
        # 读取模板已有键
        existing = set()
        if tpl.exists():
            for r in read_rows(tpl):
                key = (r.get('source_term','').strip(), r.get('target_term','').strip())
                if key[0] and key[1]:
                    existing.add(key)
        # 读取建议并过滤
        candidates = []
        for r in read_rows(sug):
            try:
                conf = float(r.get('confidence') or 0)
            except ValueError:
                conf = 0.0
            key = (r.get('source_term','').strip(), r.get('target_term','').strip())
            if conf >= args.min and key[0] and key[1] and key not in existing:
                candidates.append(r)
                existing.add(key)
        if not candidates:
            print(f"{name}: 无满足阈值的候选，跳过。")
            continue
        # 追加写入
        mode = 'a' if tpl.exists() else 'w'
        write_rows(tpl, candidates, mode=mode)
        print(f"{name}: 追加 {len(candidates)} 条到模板 -> {tpl}")

if __name__ == '__main__':
    main()

