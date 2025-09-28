#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于 Tag/Module 共现关系，自动生成候选关系（不直接写库），输出到 data/relations/suggestions/*
- TestCase→Metric (MEASURES)
- TestCase→Tool (USES_TOOL)
- Process→Tool (USES_TOOL)
- Process→Material (CONSUMES)
- Component→Symptom (HAS_SYMPTOM)

每条候选给出 score∈[0,1] 与理由（共享标签/模块数）。
"""
import csv
from pathlib import Path
from typing import List, Tuple
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "password123"

OUT_DIR = Path("data/relations/suggestions")
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUERIES = {
    "testcases_measures_metrics.csv": (
        """
        MATCH (tc:Dictionary:TestCase)-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(m:Dictionary:Metric)
        OPTIONAL MATCH (tc)-[:IN_MODULE]->(mm:Module)<-[:IN_MODULE]-(m)
        WITH tc, m, collect(DISTINCT t.name) AS tags, count(DISTINCT mm) AS sharedM
        WITH tc, m, size(tags) AS tag_overlap, sharedM
        WHERE tag_overlap >= 1
        RETURN tc.term AS source, m.term AS target, tag_overlap, sharedM
        ORDER BY tag_overlap DESC, sharedM DESC LIMIT 200
        """,
        ("source", "target", "tag_overlap", "sharedM"),
        "MEASURES"
    ),
    "testcases_uses_tools.csv": (
        """
        MATCH (tc:Dictionary:TestCase)-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(tool:Dictionary:Tool)
        OPTIONAL MATCH (tc)-[:IN_MODULE]->(mm:Module)<-[:IN_MODULE]-(tool)
        WITH tc, tool, collect(DISTINCT t.name) AS tags, count(DISTINCT mm) AS sharedM
        WITH tc, tool, size(tags) AS tag_overlap, sharedM
        WHERE tag_overlap >= 1
        RETURN tc.term AS source, tool.term AS target, tag_overlap, sharedM
        ORDER BY tag_overlap DESC, sharedM DESC LIMIT 200
        """,
        ("source", "target", "tag_overlap", "sharedM"),
        "USES_TOOL"
    ),
    "process_uses_tools.csv": (
        """
        MATCH (p:Dictionary:Process)-[:IN_MODULE]->(m:Module)<-[:IN_MODULE]-(tool:Dictionary:Tool)
        OPTIONAL MATCH (p)-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(tool)
        WITH p, tool, count(DISTINCT m) AS sharedM, collect(DISTINCT t.name) AS tags
        WITH p, tool, sharedM, size(tags) AS tag_overlap
        WHERE sharedM >= 1 OR tag_overlap >= 1
        RETURN p.term AS source, tool.term AS target, tag_overlap, sharedM
        ORDER BY sharedM DESC, tag_overlap DESC LIMIT 200
        """,
        ("source", "target", "tag_overlap", "sharedM"),
        "USES_TOOL"
    ),
    "process_consumes_materials.csv": (
        """
        MATCH (p:Dictionary:Process)-[:IN_MODULE]->(m:Module)<-[:IN_MODULE]-(mat:Dictionary:Material)
        OPTIONAL MATCH (p)-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(mat)
        WITH p, mat, count(DISTINCT m) AS sharedM, collect(DISTINCT t.name) AS tags
        WITH p, mat, sharedM, size(tags) AS tag_overlap
        WHERE sharedM >= 1 OR tag_overlap >= 1
        RETURN p.term AS source, mat.term AS target, tag_overlap, sharedM
        ORDER BY sharedM DESC, tag_overlap DESC LIMIT 200
        """,
        ("source", "target", "tag_overlap", "sharedM"),
        "CONSUMES"
    ),
    "component_has_symptom.csv": (
        """
        MATCH (c:Dictionary:Component)-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(s:Dictionary:Symptom)
        OPTIONAL MATCH (c)-[:IN_MODULE]->(m:Module)<-[:IN_MODULE]-(s)
        WITH c, s, collect(DISTINCT t.name) AS tags, count(DISTINCT m) AS sharedM
        WITH c, s, size(tags) AS tag_overlap, sharedM
        WHERE tag_overlap >= 1
        RETURN c.term AS source, s.term AS target, tag_overlap, sharedM
        ORDER BY tag_overlap DESC, sharedM DESC LIMIT 200
        """,
        ("source", "target", "tag_overlap", "sharedM"),
        "HAS_SYMPTOM"
    ),
}


def score(tag_overlap: int, sharedM: int) -> float:
    s = 0.2*min(tag_overlap, 3) + 0.3*min(sharedM, 2) + 0.5
    if s > 1.0:
        s = 1.0
    return round(s, 2)


def main():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        for filename, (cy, cols, rel) in QUERIES.items():
            print(f"Generating suggestions for {filename} …")
            rows: List[Tuple[str,str,float,str]] = []
            for rec in session.run(cy):
                src = rec[cols[0]]
                dst = rec[cols[1]]
                sc = score(rec[cols[2]], rec[cols[3]])
                rows.append((src, dst, sc, f"tags={rec[cols[2]]}; modules={rec[cols[3]]}"))
            out = OUT_DIR / filename
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open('w', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                w.writerow(["source_term","target_term","confidence","source","note"])
                for src, dst, sc, reason in rows:
                    w.writerow([src, dst, sc, "suggestion:auto", reason])
            print(f"  -> {out}  ({len(rows)} rows)")
    driver.close()

if __name__ == '__main__':
    main()

