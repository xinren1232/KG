#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 data/relations/templates/*.csv 导入跨节点关系（幂等）。
- 读取每个模板文件；忽略以 # 开头的行
- 依列映射到具体关系与标签
- 可 dry-run 统计将创建的边数量，不写入

CSV 列：source_term,target_term,confidence,source,note
节点匹配键：(:Dictionary:Label {term: <term>})

关系类型与文件名的映射：
- testcases_measures_metrics.csv      -> (TestCase)-[:MEASURES]->(Metric)
- testcases_uses_tools.csv            -> (TestCase)-[:USES_TOOL]->(Tool)
- testcases_covers_components.csv     -> (TestCase)-[:COVERS_COMPONENT]->(Component)
- process_uses_tools*.csv             -> (Process)-[:USES_TOOL]->(Tool)
- process_consumes_materials*.csv     -> (Process)-[:CONSUMES]->(Material)
- component_has_symptom.csv           -> (Component)-[:HAS_SYMPTOM]->(Symptom)

用法：
  python import_relations_from_csv.py            # 实际写入
  python import_relations_from_csv.py --dry-run  # 只统计
"""
from __future__ import annotations
import csv
import glob
import argparse
from dataclasses import dataclass
from typing import List, Tuple
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "password123"

@dataclass
class Plan:
    file: str
    src_label: str
    rel: str
    dst_label: str

MAPPING: List[Plan] = [
    Plan("data/relations/suggestions/testcases_measures_metrics.csv", "TestCase", "MEASURES", "Metric"),
    Plan("data/relations/suggestions/testcases_uses_tools.csv", "TestCase", "USES_TOOL", "Tool"),
    Plan("data/relations/suggestions/component_has_symptom.csv", "Component", "HAS_SYMPTOM", "Symptom"),
    Plan("data/relations/suggestions/process_uses_tools.csv", "Process", "USES_TOOL", "Tool"),
    Plan("data/relations/suggestions/process_consumes_materials.csv", "Process", "CONSUMES", "Material"),
]
# 支持 v2 文件名（避免 Windows 非法字符问题）
for f, src, rel, dst in [
    ("data/relations/templates/process_uses_tools*.csv", "Process", "USES_TOOL", "Tool"),
    ("data/relations/templates/process_consumes_materials*.csv", "Process", "CONSUMES", "Material"),
]:
    for matched in glob.glob(f):
        MAPPING.append(Plan(matched, src, rel, dst))

MERGE_TEMPLATE = """
MATCH (a:{src_label} {{name: $src}})
MATCH (b:{dst_label} {{name: $dst}})
MERGE (a)-[r:{rel}]->(b)
SET r.confidence = coalesce($confidence, r.confidence),
    r.source = coalesce($source, r.source),
    r.note = coalesce($note, r.note),
    r.updated_at = datetime();
"""

EXIST_TEMPLATE = """
MATCH (:{src_label} {{name: $src}})-[r:{rel}]->(:{dst_label} {{name: $dst}})
RETURN count(r) AS c
"""


def parse_row(row: dict) -> Tuple[str, str, float|None, str|None, str|None]:
    def norm(s: str|None) -> str|None:
        if s is None:
            return None
        s = s.strip()
        if not s or s.startswith('#'):
            return None
        return s
    src = norm(row.get('source_term'))
    dst = norm(row.get('target_term'))
    if not src or not dst:
        return None, None, None, None, None
    conf = row.get('confidence')
    conf_f = float(conf) if conf not in (None, '') else None
    return src, dst, conf_f, norm(row.get('source')), norm(row.get('note'))


def run_plan(driver, plan: Plan, dry_run: bool) -> Tuple[int, int, int]:
    created = 0
    skipped = 0
    missing = 0
    with open(plan.file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader((line for line in f if not line.lstrip().startswith('#')))
        with driver.session() as session:
            for row in reader:
                src, dst, conf, source, note = parse_row(row)
                if not src or not dst:
                    continue
                # 检查节点是否存在
                exist_nodes = session.run(
                    f"""
                    OPTIONAL MATCH (src:{plan.src_label} {{name:$src}})
                    OPTIONAL MATCH (dst:{plan.dst_label} {{name:$dst}})
                    RETURN src IS NOT NULL AND dst IS NOT NULL AS ok
                    """,
                    src=src, dst=dst
                ).single()["ok"]
                if not exist_nodes:
                    missing += 1
                    continue
                if dry_run:
                    # 统计是否已存在关系
                    exists = session.run(EXIST_TEMPLATE.format(src_label=plan.src_label, dst_label=plan.dst_label, rel=plan.rel), src=src, dst=dst).single()["c"]
                    if exists:
                        skipped += 1
                    else:
                        created += 1
                else:
                    session.run(MERGE_TEMPLATE.format(src_label=plan.src_label, dst_label=plan.dst_label, rel=plan.rel), src=src, dst=dst, confidence=conf, source=source, note=note)
                    created += 1
    return created, skipped, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='只统计不写入')
    args = ap.parse_args()

    if not MAPPING:
        print('没有找到任何模板文件，已跳过。')
        return

    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    total_created = total_skipped = total_missing = 0
    print("将处理以下模板文件：")
    for p in MAPPING:
        print(f" - {p.file}  => ({p.src_label})-[:{p.rel}]->({p.dst_label})")
    for plan in MAPPING:
        print(f"\n处理: {plan.file}")
        try:
            created, skipped, missing = run_plan(driver, plan, args.dry_run)
            total_created += created
            total_skipped += skipped
            total_missing += missing
            mode = 'DRY-RUN' if args.dry_run else 'WRITE'
            print(f"[{mode}] 新增(或将新增): {created}, 已存在: {skipped}, 缺少节点: {missing}")
        except FileNotFoundError:
            print("(跳过：文件不存在)")
            continue
    driver.close()
    print("\n汇总: 新增(或将新增)=%d, 已存在=%d, 缺少节点=%d" % (total_created, total_skipped, total_missing))

if __name__ == '__main__':
    main()

