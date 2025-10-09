#!/usr/bin/env python3
"""
Backfill canonical_id for core labels and add unique constraints.
- Deterministic id: <LABEL_PREFIX>_<sha1(label|name)[:8]>
- Leave existing canonical_id unchanged
- Create constraints IF NOT EXISTS
- Optionally stamps created_at/updated_at when missing
"""
import hashlib
from neo4j import GraphDatabase
import os

LABELS = [
    ("Component", "CMP"),
    ("Symptom", "SYM"),
    ("Tool", "TOL"),
    ("Process", "PRC"),
    ("TestCase", "TST"),
    ("Material", "MAT"),
    ("Role", "ROL"),
    ("Metric", "MET"),
]

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASS = os.getenv("NEO4J_PASS", "password123")

def make_id(label:str, name:str, prefix:str)->str:
    base = f"{label}|{(name or '').strip().lower()}".encode("utf-8")
    h = hashlib.sha1(base).hexdigest()[:8].upper()
    return f"{prefix}_{h}"

def main():
    driver = GraphDatabase.driver(URI, auth=(USER, PASS))
    with driver.session() as s:
        # constraints
        for label, _ in LABELS:
            cname = f"uniq_{label.lower()}_cid"
            s.run(f"CREATE CONSTRAINT {cname} IF NOT EXISTS FOR (n:{label}) REQUIRE n.canonical_id IS UNIQUE")
        # backfill
        for label, prefix in LABELS:
            q = f"MATCH (n:{label}) WHERE n.canonical_id IS NULL RETURN n.name AS name LIMIT 200000"
            rows = s.run(q).data()
            if not rows:
                continue
            cnt=0
            tx = s.begin_transaction()
            try:
                for row in rows:
                    name = row.get("name")
                    if not name:
                        continue
                    cid = make_id(label, name, prefix)
                    tx.run(f"""
                        MATCH (n:{label} {{name:$name}})
                        SET n.canonical_id=$cid,
                            n.created_at = coalesce(n.created_at, datetime()),
                            n.updated_at = datetime()
                    """, name=name, cid=cid)
                    cnt+=1
                tx.commit()
            except Exception:
                tx.rollback()
                raise
            print(f"Backfilled {cnt} nodes for {label}")
    driver.close()

if __name__ == "__main__":
    main()

