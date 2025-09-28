import csv, os
from datetime import datetime
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()  # 允许读取 .env

URI = os.environ.get("NEO4J_URI","bolt://localhost:7687")
USER= os.environ.get("NEO4J_USER","neo4j")
PWD = os.environ.get("NEO4J_PASS","password123")
driver = GraphDatabase.driver(URI, auth=(USER, PWD))

def read_rows(path):
  with open(path, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
      name = (r.get("术语") or "").strip()
      if not name: continue
      aliases = [a.strip() for a in (r.get("别名") or "").split(";") if a.strip()]
      tags = [t.strip() for t in (r.get("多标签") or "").split(";") if t.strip()]
      yield {
        "name": name,
        "aliases": aliases,
        "category": (r.get("类别") or "").strip(),
        "tags": tags,
        "definition": (r.get("备注") or "").strip(),
        "source": "dict:quality_terms.csv",
        "confidence": 0.9,
        "version": 1,
        "updated_at": datetime.utcnow().isoformat()+"Z"
      }

def merge_term(tx, t):
  tx.run("""
  MERGE (n:Term {name:$name})
  SET n.aliases     = $aliases,
      n.category    = $category,
      n.tags        = $tags,
      n.definition  = $definition,
      n.source      = $source,
      n.confidence  = $confidence,
      n.version     = $version,
      n.updated_at  = $updated_at
  """, **t)

if __name__=="__main__":
  csv_path = "data/dicts/quality_terms.csv"
  with driver.session() as s:
    for t in read_rows(csv_path):
      s.execute_write(merge_term, t)
  print("✅ Terms ingested.")
  driver.close()
