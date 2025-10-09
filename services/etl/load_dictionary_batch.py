#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量导入基座词典（Term/Category/Tag/Alias + BELONGS_TO/HAS_TAG/ALIAS_OF），
采用 UNWIND 分批写入，避免逐条 run 导致的不确定行为。
"""
from neo4j import GraphDatabase
import csv
from pathlib import Path
from datetime import datetime

URI = 'bolt://localhost:7687'
AUTH = ('neo4j', 'password123')
CSV_PATH = Path('data/dictionary/dictionary_v1.csv')
BUILD_ID = f"dict-{datetime.now().strftime('%Y%m%d')}-batch"
BATCH = 200

Q_CONSTRAINTS = [
    "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (g:Tag) REQUIRE g.name IS UNIQUE",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Alias) REQUIRE a.name IS UNIQUE",
]

Q_MERGE_CATEGORIES = "UNWIND $names AS n MERGE (:Category {name:n})"
Q_MERGE_TAGS = "UNWIND $names AS n MERGE (:Tag {name:n})"

Q_UPSERT_TERM_AND_BELONGS = (
    "UNWIND $rows AS r\n"
    "MERGE (t:Term {name:r.term, category:r.category})\n"
    "ON CREATE SET t.tags_flat=r.tags, t.note=r.note, t.source=r.source, t.version=r.version, t.ingested_at=datetime(), t.canonical=toLower(r.term)\n"
    "ON MATCH  SET t.tags_flat=r.tags, t.note=r.note, t.source=r.source, t.version=r.version\n"
    "WITH t, r\n"
    "MATCH (c:Category {name:r.category})\n"
    "MERGE (t)-[rb:BELONGS_TO]->(c)\n"
    "ON CREATE SET rb.source=r.source, rb.ingested_at=datetime(), rb.build_id=$build_id, rb.confidence=1.0\n"
)

Q_UPSERT_HAS_TAG = (
    "UNWIND $pairs AS p\n"
    "MATCH (t:Term {name:p.term, category:p.category})\n"
    "MATCH (g:Tag {name:p.tag})\n"
    "MERGE (t)-[rt:HAS_TAG]->(g)\n"
    "ON CREATE SET rt.source='dictionary_v1', rt.ingested_at=datetime(), rt.build_id=$build_id, rt.confidence=1.0\n"
)

Q_UPSERT_ALIAS = (
    "UNWIND $als AS a\n"
    "MATCH (t:Term {name:a.term, category:a.category})\n"
    "MERGE (al:Alias {name:a.alias})\n"
    "ON CREATE SET al.source='dictionary_v1', al.ingested_at=datetime(), al.build_id=$build_id\n"
    "MERGE (al)-[ra:ALIAS_OF]->(t)\n"
    "ON CREATE SET ra.source='dictionary_v1', ra.ingested_at=datetime(), ra.build_id=$build_id, ra.confidence=1.0\n"
)


def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

if __name__=='__main__':
    assert CSV_PATH.exists(), f'CSV 不存在: {CSV_PATH}'
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as s:
        # constraints except Term (由单独迁移脚本保证 NODE KEY)
        for q in Q_CONSTRAINTS:
            s.run(q)
        # read csv
        rows = list(csv.DictReader(open(CSV_PATH, newline='', encoding='utf-8')))
        # collect categories & tags
        categories = sorted({(r.get('category') or 'Uncategorized').strip() for r in rows})
        tags = sorted({t.strip() for r in rows for t in (r.get('tags') or '').split(';') if t.strip()})
        s.run(Q_MERGE_CATEGORIES, names=categories)
        if tags:
            s.run(Q_MERGE_TAGS, names=tags)
        # build params
        norm_rows = []
        tag_pairs = []
        alias_rows = []
        for r in rows:
            term = (r.get('term') or '').strip()
            cat = (r.get('category') or '').strip()
            note = (r.get('note') or '').strip()
            src = (r.get('source') or 'dictionary_v1').strip()
            ver = (r.get('version') or 'v1').strip()
            tags_flat = (r.get('tags') or '').strip()
            if not term or not cat:
                continue
            norm_rows.append({
                'term': term, 'category': cat, 'tags': tags_flat, 'note': note, 'source': src, 'version': ver
            })
            for tg in [x for x in tags_flat.split(';') if x.strip()]:
                tag_pairs.append({'term': term, 'category': cat, 'tag': tg.strip()})
            for al in [x.strip() for x in (r.get('aliases') or '').split(';') if x.strip() and x.strip()!=term]:
                alias_rows.append({'term': term, 'category': cat, 'alias': al})
        # write in batches
        for ch in chunk(norm_rows, BATCH):
            s.run(Q_UPSERT_TERM_AND_BELONGS, rows=ch, build_id=BUILD_ID)
        for ch in chunk(tag_pairs, max(1, BATCH*3)):
            s.run(Q_UPSERT_HAS_TAG, pairs=ch, build_id=BUILD_ID)
        for ch in chunk(alias_rows, BATCH*2):
            s.run(Q_UPSERT_ALIAS, als=ch, build_id=BUILD_ID)
    driver.close()
    print(f"[OK] 批量导入完成: terms={len(norm_rows)} tags={len(tag_pairs)} aliases={len(alias_rows)} (build_id={BUILD_ID})")

