#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加载基座词典 CSV 到 Neo4j，创建 Term/Category/Tag/Alias 及 BELONGS_TO/HAS_TAG/ALIAS_OF。
幂等，可重复执行。
"""
from neo4j import GraphDatabase
import csv
from pathlib import Path
from datetime import datetime

URI = 'bolt://localhost:7687'
AUTH = ('neo4j', 'password123')
CSV_PATH = Path('data/dictionary/dictionary_v1.csv')
BUILD_ID = f"dict-{datetime.now().strftime('%Y%m%d')}"

# 约束（幂等）
# 注意：Term 使用 (name, category) 复合唯一（NODE KEY）在单独迁移脚本中创建，避免与历史唯一键冲突
CONSTRAINTS = [
    "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (g:Tag) REQUIRE g.name IS UNIQUE",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Alias) REQUIRE a.name IS UNIQUE",
]

Q_MERGE_CATEGORY = "UNWIND $names AS n MERGE (:Category {name:n})"
Q_MERGE_TAG      = "UNWIND $names AS n MERGE (:Tag {name:n})"

Q_MERGE_TERM = (
    "MERGE (t:Term {name:$name, category:$category})\n"
    "ON CREATE SET t.tags_flat=$tags_flat, t.note=$note, t.source=$source, t.version=$version, t.ingested_at=datetime(), t.canonical=toLower($name)\n"
    "ON MATCH  SET t.tags_flat=$tags_flat, t.note=$note, t.source=$source, t.version=$version"
)

Q_BELONGS = (
    "MATCH (t:Term {name:$name, category:$cat}) MATCH (c:Category {name:$cat})\n"
    "MERGE (t)-[r:BELONGS_TO]->(c)\n"
    "ON CREATE SET r.source=$source, r.ingested_at=datetime(), r.build_id=$build_id, r.confidence=1.0"
)

Q_HAS_TAG = (
    "MATCH (t:Term {name:$name, category:$category}) MATCH (g:Tag {name:$tag})\n"
    "MERGE (t)-[r:HAS_TAG]->(g)\n"
    "ON CREATE SET r.source=$source, r.ingested_at=datetime(), r.build_id=$build_id, r.confidence=1.0"
)

Q_ALIAS = (
    "MATCH (t:Term {name:$name, category:$category})\n"
    "MERGE (a:Alias {name:$alias})\n"
    "ON CREATE SET a.source=$source, a.ingested_at=datetime(), a.build_id=$build_id\n"
    "MERGE (a)-[r:ALIAS_OF]->(t)\n"
    "ON CREATE SET r.source=$source, r.ingested_at=datetime(), r.build_id=$build_id, r.confidence=1.0"
)

if __name__ == '__main__':
    assert CSV_PATH.exists(), f'CSV 不存在: {CSV_PATH}'
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as s:
        # 约束
        for c in CONSTRAINTS:
            s.run(c)
        # 读取CSV
        rows = list(csv.DictReader(open(CSV_PATH, newline='', encoding='utf-8')))
        # 预清洗与收集字典
        categories = sorted({(r.get('category') or 'Uncategorized').strip() for r in rows})
        tags = sorted({t.strip() for r in rows for t in (r.get('tags') or '').split(';') if t.strip()})
        s.run(Q_MERGE_CATEGORY, names=categories)
        if tags:
            s.run(Q_MERGE_TAG, names=tags)
        # 写 Term 与边
        for r in rows:
            name = (r.get('term') or '').strip()
            if not name:
                continue
            category = (r.get('category') or 'Uncategorized').strip()
            tags_flat = (r.get('tags') or '').strip()
            note = (r.get('note') or '').strip()
            source = (r.get('source') or 'dictionary_v1').strip()
            version = (r.get('version') or 'v1').strip()
            s.run(Q_MERGE_TERM, name=name, category=category, tags_flat=tags_flat, note=note, source=source, version=version)
            s.run(Q_BELONGS, name=name, cat=category, source=source, build_id=BUILD_ID)
            for tg in [x for x in tags_flat.split(';') if x.strip()]:
                s.run(Q_HAS_TAG, name=name, category=category, tag=tg.strip(), source=source, build_id=BUILD_ID)
            aliases = [x.strip() for x in (r.get('aliases') or '').split(';') if x.strip() and x.strip()!=name]
            for al in aliases:
                s.run(Q_ALIAS, name=name, category=category, alias=al, source=source, build_id=BUILD_ID)
    driver.close()
    print(f'[OK] 词典基座导入完成：terms={len(rows)} categories={len(categories)} tags={len(tags)} (build_id={BUILD_ID})')
