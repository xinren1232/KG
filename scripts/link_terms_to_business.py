#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为现有业务节点与基座 Term 建立对齐边 SAME_AS（或 HAS_TERM）。
匹配规则：业务节点 name 与 Term.name 相同，且 Term.category == 业务标签名。
幂等，可回滚（build_id 标记）。
"""
from neo4j import GraphDatabase
from datetime import datetime

URI='bolt://localhost:7687'
AUTH=('neo4j','password123')
BUILD_ID=f'term-align-{datetime.now().strftime("%Y%m%d")}'

CATS=['Component','Symptom','Tool','Process','TestCase','Material','Role','Metric']

Q = """
UNWIND $cats AS L
MATCH (t:Term {category:L})
MATCH (n) WHERE L IN labels(n) AND coalesce(n.name,n.term) = t.name
MERGE (n)-[r:SAME_AS]->(t)
ON CREATE SET r.source='term_base', r.build_id=$build_id, r.created_at=datetime(), r.confidence=1.0
RETURN L AS label, count(r) AS created
"""

if __name__=='__main__':
    driver=GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as s:
        res = s.run(Q, cats=CATS, build_id=BUILD_ID).data()
        for row in res:
            print(f"{row['label']}: 新建/幂等 {row['created']} 条 SAME_AS")
    driver.close()
    print('[OK] 业务节点与 Term 对齐完成')
