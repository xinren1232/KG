#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为新增 TestCase 基于标签创建低风险 RELATED_TO 关系（inferred=true），以降低孤立节点。
- 策略：按标签交集创建 RELATED_TO，带证据字段（source/rule/build_id/created_at/common_tags/common_count/confidence）
- 置信度：common_count / max(1, size(t.tags))
- 去重：MERGE 幂等，重复执行安全
"""

from neo4j import GraphDatabase
from datetime import datetime

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123")

BUILD_ID = f"auto-tag-relations-{datetime.utcnow().strftime('%Y%m%d')}"

CY_LIST = [
    {
        "name": "TestCase->Metric",
        "cypher": """
        MATCH (t:TestCase) WHERE t.tags IS NOT NULL AND size(t.tags) > 0
        MATCH (m:Metric)   WHERE m.tags IS NOT NULL AND size(m.tags) > 0
        WITH t, m, [x IN t.tags WHERE x IN m.tags] AS common, size(t.tags) AS tsize
        WITH t, m, common, size(common) AS score, toFloat(size(common))/toFloat( CASE WHEN tsize=0 THEN 1 ELSE tsize END ) AS conf
        WHERE score >= 2 AND conf >= 0.4
        ORDER BY t.name, score DESC
        WITH t, collect({node:m, common:common, score:score, conf:conf})[0..5] AS best
        UNWIND best AS b
        WITH t, b.node AS n, b.common AS common, b.score AS score, b.conf AS conf
        MERGE (t)-[r:RELATED_TO]->(n)
        ON CREATE SET r.inferred = true,
                      r.source = 'tag_similarity',
                      r.rule = 'tag_overlap',
                      r.build_id = $build_id,
                      r.created_at = datetime(),
                      r.common_tags = common,
                      r.common_count = score,
                      r.confidence = conf
        RETURN count(r) AS created
        """
    },
    {
        "name": "TestCase->Symptom",
        "cypher": """
        MATCH (t:TestCase) WHERE t.tags IS NOT NULL AND size(t.tags) > 0
        MATCH (s:Symptom)  WHERE s.tags IS NOT NULL AND size(s.tags) > 0
        WITH t, s, [x IN t.tags WHERE x IN s.tags] AS common, size(t.tags) AS tsize
        WITH t, s, common, size(common) AS score, toFloat(size(common))/toFloat( CASE WHEN tsize=0 THEN 1 ELSE tsize END ) AS conf
        WHERE score >= 2 AND conf >= 0.4
        ORDER BY t.name, score DESC
        WITH t, collect({node:s, common:common, score:score, conf:conf})[0..5] AS best
        UNWIND best AS b
        WITH t, b.node AS n, b.common AS common, b.score AS score, b.conf AS conf
        MERGE (t)-[r:RELATED_TO]->(n)
        ON CREATE SET r.inferred = true,
                      r.source = 'tag_similarity',
                      r.rule = 'tag_overlap',
                      r.build_id = $build_id,
                      r.created_at = datetime(),
                      r.common_tags = common,
                      r.common_count = score,
                      r.confidence = conf
        RETURN count(r) AS created
        """
    },
    {
        "name": "TestCase->Component",
        "cypher": """
        MATCH (t:TestCase) WHERE t.tags IS NOT NULL AND size(t.tags) > 0
        MATCH (c:Component) WHERE c.tags IS NOT NULL AND size(c.tags) > 0
        WITH t, c, [x IN t.tags WHERE x IN c.tags] AS common, size(t.tags) AS tsize
        WITH t, c, common, size(common) AS score, toFloat(size(common))/toFloat( CASE WHEN tsize=0 THEN 1 ELSE tsize END ) AS conf
        WHERE score >= 2 AND conf >= 0.4
        ORDER BY t.name, score DESC
        WITH t, collect({node:c, common:common, score:score, conf:conf})[0..5] AS best
        UNWIND best AS b
        WITH t, b.node AS n, b.common AS common, b.score AS score, b.conf AS conf
        MERGE (t)-[r:RELATED_TO]->(n)
        ON CREATE SET r.inferred = true,
                      r.source = 'tag_similarity',
                      r.rule = 'tag_overlap',
                      r.build_id = $build_id,
                      r.created_at = datetime(),
                      r.common_tags = common,
                      r.common_count = score,
                      r.confidence = conf
        RETURN count(r) AS created
        """
    },
    {
        "name": "TestCase->Tool",
        "cypher": """
        MATCH (t:TestCase) WHERE t.tags IS NOT NULL AND size(t.tags) > 0
        MATCH (l:Tool)     WHERE l.tags IS NOT NULL AND size(l.tags) > 0
        WITH t, l, [x IN t.tags WHERE x IN l.tags] AS common, size(t.tags) AS tsize
        WITH t, l, common, size(common) AS score, toFloat(size(common))/toFloat( CASE WHEN tsize=0 THEN 1 ELSE tsize END ) AS conf
        WHERE score >= 3 AND conf >= 0.5
        ORDER BY t.name, score DESC
        WITH t, collect({node:l, common:common, score:score, conf:conf})[0..3] AS best
        UNWIND best AS b
        WITH t, b.node AS n, b.common AS common, b.score AS score, b.conf AS conf
        MERGE (t)-[r:RELATED_TO]->(n)
        ON CREATE SET r.inferred = true,
                      r.source = 'tag_similarity',
                      r.rule = 'tag_overlap',
                      r.build_id = $build_id,
                      r.created_at = datetime(),
                      r.common_tags = common,
                      r.common_count = score,
                      r.confidence = conf
        RETURN count(r) AS created
        """
    }
]


def main():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        total_created = 0
        for item in CY_LIST:
            name = item["name"]
            cypher = item["cypher"]
            # 将注释风格 // 替换为 /* */ 以兼容 Neo4j
            cypher = cypher.replace("// 工具阈值稍高，避免泛化", "/* 工具阈值稍高，避免泛化 */")
            result = session.run(cypher, build_id=BUILD_ID)
            record = result.single()
            created = record["created"] if record else 0
            print(f"✅ {name}: 新建/幂等 {created} 条")
            total_created += created

        print(f"\n[OK] 标签相似度建边完成，合计新建/幂等 {total_created} 条 (build_id={BUILD_ID})")

if __name__ == "__main__":
    main()

