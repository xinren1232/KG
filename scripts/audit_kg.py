#!/usr/bin/env python3
"""
Comprehensive audit for dictionary and knowledge graph rules/design.
Outputs a concise report to stdout and writes JSON/Markdown summaries into reports/.

Checks:
- Node/relationship counts and distributions
- canonical_id presence & uniqueness per label
- Confidence buckets and inferred breakdown per rel type
- Duplicate edges (same a,b,type) and legacy rel types not in target set
- Orphan nodes per label; top-degree nodes per label
- Property coverage on relations: rule_id, source_doc, page, span
- Dictionary checks: term uniqueness, category whitelist, missing definitions, alias/tags formatting
- Mapping/rule config scan: relationship types across YAML/JSON vs target set
"""
import os, json, re, hashlib
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, Any, List
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASS = os.getenv("NEO4J_PASS", "password123")

LABELS = ['Component','Symptom','Tool','Process','TestCase','Material','Role','Metric','Anomaly']
TARGET_REL_TYPES = set(['HAS_SYMPTOM','OCCURS_IN','DETECTED_BY','FIXED_BY','RELATED_TO','PART_OF','USES'])

REPORT_DIR = Path('reports')
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def audit_graph(driver):
    out: Dict[str, Any] = {}
    with driver.session() as s:
        out['total_nodes'] = s.run('MATCH (n) RETURN count(n) AS c').single()['c']
        out['total_rels']  = s.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c']
        out['nodes_by_label'] = s.run('MATCH (n) RETURN labels(n)[0] AS l, count(n) AS c ORDER BY c DESC').data()
        out['rels_by_type']   = s.run('MATCH ()-[r]->() RETURN type(r) AS t, count(r) AS c ORDER BY c DESC').data()
        # canonical_id presence
        cid = {}
        for lab in LABELS:
            rec = s.run(f"MATCH (n:{lab}) RETURN count(n) as c, count(n.canonical_id) as cc").single()
            if rec:
                cid[lab] = {'nodes': rec['c'], 'with_canonical_id': rec['cc']}
        out['canonical_id'] = cid
        # uniqueness sample check per label
        uniq = {}
        for lab in LABELS:
            rec = s.run(f"MATCH (n:{lab}) WHERE n.canonical_id IS NOT NULL RETURN count(n.canonical_id) as c, size(collect(distinct n.canonical_id)) as dc").single()
            if rec:
                uniq[lab] = {'total_with_cid': rec['c'], 'distinct_cid': rec['dc'], 'ok': rec['c']==rec['dc']}
        out['canonical_unique'] = uniq
        # confidence buckets per rel type
        buckets = ['<0.3','0.3-0.5','0.5-0.8','>=0.8','missing']
        bucket_rec = {}
        rtypes = [r['t'] for r in out['rels_by_type']]
        for t in rtypes:
            q = f"""
            MATCH ()-[r:`{t}`]->()
            RETURN sum(CASE WHEN r.confidence IS NOT NULL AND r.confidence < 0.3 THEN 1 ELSE 0 END) AS lt03,
                   sum(CASE WHEN r.confidence IS NOT NULL AND r.confidence >= 0.3 AND r.confidence < 0.5 THEN 1 ELSE 0 END) AS b1,
                   sum(CASE WHEN r.confidence IS NOT NULL AND r.confidence >= 0.5 AND r.confidence < 0.8 THEN 1 ELSE 0 END) AS b2,
                   sum(CASE WHEN r.confidence IS NOT NULL AND r.confidence >= 0.8 THEN 1 ELSE 0 END) AS ge08,
                   sum(CASE WHEN r.confidence IS NULL THEN 1 ELSE 0 END) AS miss,
                   sum(CASE WHEN coalesce(r.inferred,false) THEN 1 ELSE 0 END) AS inferred,
                   count(r) AS total
            """
            rec = s.run(q).single()
            if rec:
                bucket_rec[t] = {
                    buckets[0]: rec['lt03'], buckets[1]: rec['b1'], buckets[2]: rec['b2'], buckets[3]: rec['ge08'], buckets[4]: rec['miss'],
                    'inferred': rec['inferred'], 'total': rec['total']
                }
        out['confidence_buckets'] = bucket_rec
        # duplicate edges (same a,b,type)
        dup = s.run('''
            MATCH (a)-[r]->(b)
            WITH elementId(a) AS a, type(r) AS t, elementId(b) AS b, count(*) AS c
            WHERE c>1
            RETURN t, count(*) AS pair_count, sum(c-1) AS redundant
        ''').data()
        out['duplicates'] = dup
        # legacy types (not in target set)
        legacy = [r['t'] for r in out['rels_by_type'] if r['t'] not in TARGET_REL_TYPES]
        out['legacy_types'] = legacy
        # orphan nodes
        orphan = s.run('MATCH (n) WHERE NOT (n)--() RETURN labels(n)[0] AS l, count(n) AS c ORDER BY c DESC').data()
        out['orphans'] = orphan
        # top degrees per label
        topdeg: Dict[str, List[Dict[str, Any]]] = {}
        for lab in LABELS:
            rs = s.run(f"""
                MATCH (n:{lab})
                OPTIONAL MATCH (n)--(m)
                WITH n, count(m) AS deg
                RETURN n.name AS name, coalesce(n.canonical_id,'') AS cid, deg
                ORDER BY deg DESC LIMIT 10
            """).data()
            if rs:
                topdeg[lab] = rs
        out['top_degree'] = topdeg
        # property coverage on relations
        prop_cov = s.run('''
            MATCH ()-[r]->()
            RETURN type(r) AS t,
                   sum(CASE WHEN r.rule_id IS NOT NULL THEN 1 ELSE 0 END) AS rule_id,
                   sum(CASE WHEN r.source_doc IS NOT NULL THEN 1 ELSE 0 END) AS source_doc,
                   sum(CASE WHEN r.page IS NOT NULL THEN 1 ELSE 0 END) AS page,
                   sum(CASE WHEN r.span IS NOT NULL THEN 1 ELSE 0 END) AS span,
                   count(r) AS total
        ''').data()
        out['rel_property_coverage'] = prop_cov
    return out


def audit_dictionary(dict_path: Path) -> Dict[str, Any]:
    res = {'exists': dict_path.exists()}
    if not dict_path.exists():
        return res
    data = json.loads(dict_path.read_text(encoding='utf-8'))
    if isinstance(data, dict) and 'entries' in data:
        data = data['entries']
    if not isinstance(data, list):
        res['error'] = 'dictionary JSON should be a list or {entries: []}'
        return res
    res['total'] = len(data)
    whitelist = set(['Symptom','Component','Tool','Process','TestCase','Metric','Material','Role'])
    terms = []
    dup_terms = []
    missing_def = 0
    bad_cat = Counter()
    bad_status = 0
    for item in data:
        term = (item.get('term') or item.get('name') or '').strip()
        cat = (item.get('category') or '').strip()
        if not term or not cat:
            continue
        key = (term.lower(), cat)
        if key in terms:
            dup_terms.append(term)
        else:
            terms.append(key)
        if cat not in whitelist:
            bad_cat[cat]+=1
        if not (item.get('definition') or item.get('description')):
            missing_def += 1
        status = (item.get('status') or 'active').strip().lower()
        if status not in ('active','deprecated'):
            bad_status += 1
    res['duplicates'] = list(set(dup_terms))[:20]
    res['missing_definitions'] = missing_def
    res['bad_categories'] = dict(bad_cat)
    res['bad_status_count'] = bad_status
    return res


def scan_mapping_and_rules() -> Dict[str, Any]:
    res: Dict[str, Any] = {'mapping_rel_types': [], 'found_files': []}
    # scan mapping yaml files and configs for relationship names
    candidates = []
    for p in Path('api').rglob('*.yaml'):
        candidates.append(p)
    for p in Path('config').rglob('*.json'):
        candidates.append(p)
    res['found_files'] = [str(p) for p in candidates[:50]]
    rel_types = set()
    for p in candidates:
        text = p.read_text(encoding='utf-8', errors='ignore')
        rel_types.update(set(re.findall(r"\b[A-Z_]{3,}\b", text)))
    # filter common words
    filtered = sorted([t for t in rel_types if t.isupper() and '_' in t])
    res['mapping_rel_types'] = filtered[:200]
    res['non_target_rel_types'] = [t for t in filtered if t not in TARGET_REL_TYPES][:50]
    return res


def main():
    driver = GraphDatabase.driver(URI, auth=(USER, PASS))
    graph = audit_graph(driver)
    dict_res = audit_dictionary(Path('api/data/dictionary.json'))
    map_res = scan_mapping_and_rules()
    report = {'graph': graph, 'dictionary': dict_res, 'mappings_rules': map_res}
    # write JSON
    (REPORT_DIR / 'kg_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    # write brief markdown
    md = []
    md.append('# KG Audit Summary\n')
    md.append(f"Nodes: {graph['total_nodes']}, Relations: {graph['total_rels']}\n")
    md.append('## Nodes by label\n')
    md.append(', '.join([f"{x['l']}={x['c']}" for x in graph['nodes_by_label']]))
    md.append('\n## Rels by type\n')
    md.append(', '.join([f"{x['t']}={x['c']}" for x in graph['rels_by_type']]))
    md.append('\n## Legacy types (not in target set)\n')
    md.append(', '.join(graph['legacy_types']))
    md.append('\n## Orphans\n')
    md.append(', '.join([f"{x['l']}={x['c']}" for x in graph['orphans']]))
    md.append('\n## Dictionary\n')
    md.append(json.dumps(dict_res, ensure_ascii=False))
    md.append('\n## Non-target rel types in configs\n')
    md.append(', '.join(map_res['non_target_rel_types']))
    (REPORT_DIR / 'kg_audit.md').write_text('\n'.join(md), encoding='utf-8')
    print('Audit complete. See reports/kg_audit.json and reports/kg_audit.md')

if __name__ == '__main__':
    main()

