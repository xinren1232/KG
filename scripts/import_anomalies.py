#!/usr/bin/env python3
"""
Import Anomaly nodes and relationships from CSV/JSON.
Supported edges:
- HAS_SYMPTOM (Anomaly -> Symptom)
- OCCURS_IN   (Anomaly -> Component/Process/Material)
- DETECTED_BY (Anomaly -> TestCase/Tool/Metric)
- FIXED_BY    (Anomaly -> Process/Tool/Material)

Matching strategy:
- Prefer canonical_id columns (e.g., anomaly_cid, symptom_cid, component_cid, ...)
- Fallback to name matching on existing nodes
- Only Anomaly nodes are created (upsert); other endpoint nodes must exist

Usage:
  python scripts/import_anomalies.py --csv data/anomalies.csv --dry-run
  python scripts/import_anomalies.py --csv data/anomalies.csv --apply --default-conf 0.9 --build B2025.01

CSV columns (any subset):
  anomaly, anomaly_cid, symptom, symptom_cid,
  component, component_cid, process, process_cid,
  testcase, testcase_cid, tool, tool_cid, metric, metric_cid,
  fix_process, fix_process_cid, fix_tool, fix_tool_cid, fix_material, fix_material_cid,
  confidence, rule_id, source_doc, page, span

"""
import csv
import json
import os
import sys
import argparse
import hashlib
from typing import Dict, Any, Optional
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASS = os.getenv("NEO4J_PASS", "password123")

LABEL_PREFIX = {
    'Anomaly': 'ANO', 'Symptom': 'SYM', 'Component': 'CMP', 'Process': 'PRC',
    'TestCase': 'TST', 'Tool': 'TOL', 'Material': 'MAT', 'Metric': 'MET'
}

def make_cid(label: str, name: str) -> str:
    base = f"{label}|{(name or '').strip().lower()}".encode('utf-8')
    return f"{LABEL_PREFIX[label]}_{hashlib.sha1(base).hexdigest()[:8].upper()}"


def resolve_node(tx, label: str, cid: Optional[str], name: Optional[str]):
    if cid:
        rec = tx.run(f"MATCH (n:{label} {{canonical_id:$cid}}) RETURN elementId(n) AS id, n.name AS name", cid=cid).single()
        if rec: return rec
    if name:
        rec = tx.run(f"MATCH (n:{label} {{name:$name}}) RETURN elementId(n) AS id, n.name AS name", name=name).single()
        if rec: return rec
    return None


def upsert_anomaly(tx, name: str, cid: Optional[str], audit: Dict[str,Any]):
    if not cid:
        cid = make_cid('Anomaly', name)
    tx.run(
        """
        MERGE (a:Anomaly {canonical_id:$cid})
        ON CREATE SET a.name=$name, a.created_at=datetime(), a.source_doc=$doc
        ON MATCH  SET a.name=coalesce(a.name,$name), a.updated_at=datetime()
        """,
        cid=cid, name=name, doc=audit.get('source_doc')
    )
    return cid


def merge_rel(tx, rel: str, aid: str, to_label: str, to_eid: str, props: Dict[str,Any]):
    q = f"""
    MATCH (a:Anomaly {{canonical_id:$aid}})
    MATCH (b) WHERE elementId(b)=$bid AND '{to_label}' IN labels(b)
    MERGE (a)-[r:{rel}]->(b)
    SET r.confidence=$conf,
        r.rule_id=$rule_id,
        r.source_doc=$doc,
        r.page=$page,
        r.span=$span,
        r.inferred=coalesce(r.inferred,false),
        r.evidence_count=coalesce(r.evidence_count,0)+1,
        r.created_at=coalesce(r.created_at, datetime()),
        r.updated_at=datetime(),
        r.build_id=$build
    """
    tx.run(q, aid=aid, bid=to_eid, conf=props.get('confidence'), rule_id=props.get('rule_id'),
           doc=props.get('source_doc'), page=props.get('page'), span=props.get('span'), build=props.get('build_id'))


def process_row(tx, row: Dict[str,str], default_conf: float, build_id: Optional[str], dry: bool):
    audit = {
        'source_doc': row.get('source_doc') or 'import_csv',
        'page': row.get('page'),
        'span': row.get('span'),
        'build_id': build_id
    }
    conf = float(row.get('confidence') or default_conf)

    # ensure anomaly exists
    aname = row.get('anomaly') or row.get('anomaly_name')
    if not aname and not row.get('anomaly_cid'):
        return { 'status': 'skip', 'reason': 'missing anomaly' }

    aid = row.get('anomaly_cid')
    if not dry:
        aid = upsert_anomaly(tx, aname or 'Unknown', aid, audit)
    else:
        aid = aid or make_cid('Anomaly', aname or 'Unknown')

    stats = {'HAS_SYMPTOM':0,'OCCURS_IN':0,'DETECTED_BY':0,'FIXED_BY':0}

    def try_link(label_key: str, label: str, rel: str, name_key: str, cid_key: str):
        nonlocal stats
        target = resolve_node(tx, label, row.get(cid_key), row.get(name_key))
        if target:
            if not dry:
                merge_rel(tx, rel, aid, label, target['id'], {**audit, 'confidence':conf, 'rule_id': row.get('rule_id')})
            stats[rel]+=1

    # HAS_SYMPTOM
    try_link('Symptom','Symptom','HAS_SYMPTOM','symptom','symptom_cid')
    # OCCURS_IN (Component/Process/Material)
    for pair in [('Component','component','component_cid'), ('Process','process','process_cid'), ('Material','material','material_cid')]:
        try_link(pair[0], pair[0], 'OCCURS_IN', pair[1], pair[2])
    # DETECTED_BY (TestCase/Tool/Metric)
    for pair in [('TestCase','testcase','testcase_cid'), ('Tool','tool','tool_cid'), ('Metric','metric','metric_cid')]:
        try_link(pair[0], pair[0], 'DETECTED_BY', pair[1], pair[2])
    # FIXED_BY (Process/Tool/Material)
    for pair in [('Process','fix_process','fix_process_cid'), ('Tool','fix_tool','fix_tool_cid'), ('Material','fix_material','fix_material_cid')]:
        try_link(pair[0], pair[0], 'FIXED_BY', pair[1], pair[2])

    return {'status':'ok', **stats}


def run():
    ap = argparse.ArgumentParser(description='Import anomalies and relations')
    ap.add_argument('--csv', nargs='+', help='CSV file(s) to import')
    ap.add_argument('--json', nargs='+', help='JSON file(s) to import')
    ap.add_argument('--default-conf', type=float, default=0.9)
    ap.add_argument('--build', dest='build_id', type=str, default=None)
    ap.add_argument('--apply', action='store_true', help='Write changes to DB')
    ap.add_argument('--dry-run', action='store_true', help='Do not write changes')
    args = ap.parse_args()
    dry = not args.apply or args.dry_run

    driver = GraphDatabase.driver(URI, auth=(USER, PASS))
    total = {'rows':0,'ok':0,'skip':0,'HAS_SYMPTOM':0,'OCCURS_IN':0,'DETECTED_BY':0,'FIXED_BY':0}

    def rows_iter():
        if args.csv:
            for path in args.csv:
                with open(path, newline='', encoding='utf-8') as f:
                    for row in csv.DictReader(f):
                        yield row
        if args.json:
            for path in args.json:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for row in (data if isinstance(data,list) else data.get('items',[])):
                        yield row

    with driver.session() as s:
        tx = s.begin_transaction()
        for row in rows_iter():
            total['rows']+=1
            res = process_row(tx, row, args.default_conf, args.build_id, dry)
            if res['status']=='ok':
                total['ok']+=1
                for k in ('HAS_SYMPTOM','OCCURS_IN','DETECTED_BY','FIXED_BY'):
                    total[k]+=res[k]
            else:
                total['skip']+=1
        if not dry:
            tx.commit()
        else:
            tx.rollback()
    driver.close()

    mode = 'DRY-RUN' if dry else 'APPLY'
    print(f"{mode} summary: {total}")

if __name__ == '__main__':
    run()

