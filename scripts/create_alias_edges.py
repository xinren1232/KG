#!/usr/bin/env python3
"""
Create alias semantic edges for compatibility:
- USES_TOOL  -> USES (role='tool')
- CONSUMES   -> USES (role='material')
- MEASURES   -> DETECTED_BY (role='metric')
Properties are merged; confidence/inferred preserved.
Idempotent MERGE writes.
"""
from neo4j import GraphDatabase
import os

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASS = os.getenv("NEO4J_PASS", "password123")

def run():
    driver = GraphDatabase.driver(URI, auth=(USER, PASS))
    with driver.session() as s:
        # USES_TOOL -> USES(role='tool')
        s.run(
            """
            MATCH (a)-[r:USES_TOOL]->(b)
            MERGE (a)-[u:USES]->(b)
            SET u.role = 'tool',
                u.confidence = coalesce(u.confidence, r.confidence),
                u.inferred   = coalesce(u.inferred, r.inferred),
                u.rule       = coalesce(u.rule, r.rule),
                u.rule_id    = coalesce(u.rule_id, r.rule_id),
                u.source_doc = coalesce(u.source_doc, r.source_doc),
                u.page       = coalesce(u.page, r.page),
                u.span       = coalesce(u.span, r.span),
                u.created_at = coalesce(u.created_at, datetime()),
                u.updated_at = datetime()
            """
        )
        # CONSUMES -> USES(role='material')
        s.run(
            """
            MATCH (a)-[r:CONSUMES]->(b)
            MERGE (a)-[u:USES]->(b)
            SET u.role = 'material',
                u.confidence = coalesce(u.confidence, r.confidence),
                u.inferred   = coalesce(u.inferred, r.inferred),
                u.rule       = coalesce(u.rule, r.rule),
                u.rule_id    = coalesce(u.rule_id, r.rule_id),
                u.source_doc = coalesce(u.source_doc, r.source_doc),
                u.page       = coalesce(u.page, r.page),
                u.span       = coalesce(u.span, r.span),
                u.created_at = coalesce(u.created_at, datetime()),
                u.updated_at = datetime()
            """
        )
        # MEASURES -> DETECTED_BY(role='metric')
        s.run(
            """
            MATCH (a)-[r:MEASURES]->(m:Metric)
            MERGE (a)-[d:DETECTED_BY]->(m)
            SET d.role = 'metric',
                d.confidence = coalesce(d.confidence, r.confidence),
                d.inferred   = coalesce(d.inferred, r.inferred),
                d.rule       = coalesce(d.rule, r.rule),
                d.rule_id    = coalesce(d.rule_id, r.rule_id),
                d.source_doc = coalesce(d.source_doc, r.source_doc),
                d.page       = coalesce(d.page, r.page),
                d.span       = coalesce(d.span, r.span),
                d.created_at = coalesce(d.created_at, datetime()),
                d.updated_at = datetime()
            """
        )
    driver.close()

if __name__ == "__main__":
    run()

