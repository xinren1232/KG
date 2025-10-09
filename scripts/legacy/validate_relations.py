#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate relation counts and show top connected items.
"""
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "password123"

QUERIES = {
    'total_relationships': "MATCH ()-[r]->() RETURN count(r) AS c",
    'MEASURES': "MATCH ()-[r:MEASURES]->() RETURN count(r) AS c",
    'USES_TOOL': "MATCH ()-[r:USES_TOOL]->() RETURN count(r) AS c",
    'COVERS_COMPONENT': "MATCH ()-[r:COVERS_COMPONENT]->() RETURN count(r) AS c",
    'CONSUMES': "MATCH ()-[r:CONSUMES]->() RETURN count(r) AS c",
    'HAS_SYMPTOM': "MATCH ()-[r:HAS_SYMPTOM]->() RETURN count(r) AS c",
}

TOPS = {
    'Top TestCases': (
        """
        MATCH (tc:Dictionary:TestCase)-[r]->() RETURN tc.term AS tc, count(r) AS cnt
        ORDER BY cnt DESC LIMIT 20
        """,
        ("tc", "cnt")
    ),
    'Top Tools': (
        """
        MATCH (:Dictionary)-[:USES_TOOL]->(t:Dictionary:Tool)
        RETURN t.term AS tool, count(*) AS cnt ORDER BY cnt DESC LIMIT 20
        """,
        ("tool", "cnt")
    ),
}


def main():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        print("Counts:")
        for k, q in QUERIES.items():
            c = session.run(q).single()["c"]
            print(f" - {k}: {c}")
        print("\nTop items:")
        for title, (q, cols) in TOPS.items():
            print(f"\n{title}:")
            for rec in session.run(q):
                print("   ", rec[cols[0]], rec[cols[1]])
    driver.close()

if __name__ == '__main__':
    main()

