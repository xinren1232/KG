#!/usr/bin/env python3
"""
Neo4j upsert writer for the Quality Knowledge Graph.
- MERGE nodes by key
- MERGE relationships per design:
  * Product -[:HAS_BUILD]-> Build
  * Anomaly -[:OBSERVED_IN]-> Build
  * Anomaly -[:AFFECTS]-> Component
  * Anomaly -[:HAS_SYMPTOM]-> Symptom
- Idempotent: re-running does not duplicate nodes/edges
"""
from __future__ import annotations
from typing import Dict, List, Optional
from neo4j import GraphDatabase

class Neo4jUpserter:
    def __init__(self, uri: str="bolt://localhost:7687", user: str="neo4j", password: str="password"):
        self._driver = None
        self._err = None
        try:
            self._driver = GraphDatabase.driver(uri, auth=(user, password))
            # try open a session quickly to validate
            with self._driver.session() as s:
                s.run("RETURN 1")
        except Exception as e:
            self._err = e
            self._driver = None
            print(f"[WARN] Neo4j not available: {e}")

    def close(self):
        try:
            if self._driver:
                self._driver.close()
        except Exception:
            pass

    def upsert_anomaly_bundle(self, rec: Dict):
        """rec shape from normalize_anomaly_rows:
        {
          'anomaly': {'key': akey, 'title': ..., 'severity': ...},
          'product': {'key': pkey, 'name': ...},
          'build': {'key': bkey, 'name': ...},
          'component': {'key': ckey, 'name': ...},
          'symptom': {'key': skey, 'name': ...},
        }
        """
        if not self._driver:
            print(f"[DRY] upsert anomaly bundle (no Neo4j): {rec['anomaly']['key']}")
            return
        with self._driver.session() as s:
            s.execute_write(self._tx_upsert_anomaly_bundle, rec)

    @staticmethod
    def _tx_upsert_anomaly_bundle(tx, rec: Dict):
        a = rec['anomaly']; p = rec['product']; b = rec['build']; c = rec['component']; s = rec['symptom']
        cypher = """
        MERGE (prod:Entity:Product {key: $pkey})
          ON CREATE SET prod.name = coalesce($pname, ''), prod.created_at = datetime(),
                        prod.source = $source, prod.doc_id = $doc_id, prod.created_by = $created_by
          ON MATCH  SET prod.name = coalesce(prod.name, $pname), prod.updated_at = datetime()
        MERGE (b:Entity:Build {key: $bkey})
          ON CREATE SET b.name = coalesce($bname, ''), b.created_at = datetime(),
                        b.source = $source, b.doc_id = $doc_id, b.created_by = $created_by
          ON MATCH  SET b.name = coalesce(b.name, $bname), b.updated_at = datetime()
        MERGE (prod)-[:HAS_BUILD {source: $source, created_at: datetime()}]->(b)

        MERGE (comp:Entity:Component {key: $ckey})
          ON CREATE SET comp.name = coalesce($cname, ''), comp.created_at = datetime(),
                        comp.source = $source, comp.doc_id = $doc_id, comp.created_by = $created_by
          ON MATCH  SET comp.name = coalesce(comp.name, $cname), comp.updated_at = datetime()

        MERGE (sym:Entity:Symptom {key: $skey})
          ON CREATE SET sym.name = coalesce($sname, ''), sym.created_at = datetime(),
                        sym.source = $source, sym.doc_id = $doc_id, sym.created_by = $created_by
          ON MATCH  SET sym.name = coalesce(sym.name, $sname), sym.updated_at = datetime()

        MERGE (an:Entity:Anomaly {key: $akey})
          ON CREATE SET an.title = coalesce($atitle, ''), an.severity = $aseverity, an.created_at = datetime(),
                        an.source = $source, an.doc_id = $doc_id, an.created_by = $created_by
          ON MATCH  SET an.title = coalesce(an.title, $atitle), an.severity = coalesce(an.severity, $aseverity),
                        an.updated_at = datetime()

        MERGE (an)-[:OBSERVED_IN {source: $source, created_at: datetime()}]->(b)
        MERGE (an)-[:AFFECTS {source: $source, created_at: datetime()}]->(comp)
        MERGE (an)-[:HAS_SYMPTOM {source: $source, created_at: datetime()}]->(sym)
        """
        # Add metadata to params
        metadata = rec.get('metadata', {})
        params = {
            'pkey': p['key'], 'pname': p.get('name',''),
            'bkey': b['key'], 'bname': b.get('name',''),
            'ckey': c['key'], 'cname': c.get('name',''),
            'skey': s['key'], 'sname': s.get('name',''),
            'akey': a['key'], 'atitle': a.get('title',''), 'aseverity': a.get('severity',''),
            'source': metadata.get('source', 'excel'),
            'doc_id': metadata.get('doc_id', ''),
            'created_by': metadata.get('created_by', 'etl_system')
        }
        tx.run(cypher, **params)

    def upsert_testcase_bundle(self, rec: Dict):
        """Optionally upsert testcase + component link (OWNED_BY later if owner present)."""
        if not self._driver:
            print(f"[DRY] upsert testcase bundle (no Neo4j): {rec['testcase']['key']}")
            return
        with self._driver.session() as s:
            s.execute_write(self._tx_upsert_testcase_bundle, rec)

    @staticmethod
    def _tx_upsert_testcase_bundle(tx, rec: Dict):
        tc = rec['testcase']; comp = rec.get('component')
        cypher = """
        MERGE (tc:Entity:TestCase {key: $tkey})
          ON CREATE SET tc.title = coalesce($ttitle,''), tc.priority = $tpriority, tc.created_at = datetime()
          ON MATCH  SET tc.title = coalesce(tc.title,$ttitle), tc.priority = coalesce(tc.priority,$tpriority)
        """
        params = {'tkey': tc['key'], 'ttitle': tc.get('title',''), 'tpriority': tc.get('priority','')}
        if comp:
            cypher += """
            MERGE (c:Entity:Component {key: $ckey})
              ON CREATE SET c.name = coalesce($cname,''), c.created_at = datetime()
              ON MATCH  SET c.name = coalesce(c.name,$cname)
            MERGE (tc)-[:BELONGS_TO]->(c)
            """
            params.update({'ckey': comp['key'], 'cname': comp.get('name','')})
        tx.run(cypher, **params)

