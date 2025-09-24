#!/usr/bin/env python3
"""
Upsert writer to Neo4j for the Quality KG
- MERGE nodes by key (idempotent)
- Create required relationships for anomalies
- Maintain Product-[:HAS_BUILD]->Build linkage
"""
from __future__ import annotations
from typing import Dict, Optional
from neo4j import GraphDatabase
from .normalizer import Normalizer

class UpsertWriter:
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.norm = Normalizer()

    def close(self):
        self.driver.close()

    def _run(self, cypher: str, params: Dict):
        with self.driver.session() as s:
            return s.run(cypher, **params)

    def upsert_anomaly_row(self, row: Dict[str, str]) -> None:
        """Row keys: AnomalyID, Title, Severity, Product, Build, Component, Symptom"""
        anomaly_id = row.get('AnomalyID') or ''
        if not anomaly_id:
            return
        title = row.get('Title') or ''
        severity = row.get('Severity') or ''
        product = row.get('Product') or ''
        build = row.get('Build') or ''
        component_raw = row.get('Component') or ''
        symptom_raw = row.get('Symptom') or ''

        component = self.norm.norm_component(component_raw)
        symptom = self.norm.norm_symptom(symptom_raw)

        # keys
        a_key = self.norm.make_key('Anomaly', anomaly_id, {'code': anomaly_id})
        p_key = self.norm.make_key('Product', product)
        b_key = self.norm.make_key('Build', build, {'version': build})
        c_key = self.norm.make_key('Component', component)
        s_key = self.norm.make_key('Symptom', symptom)

        cypher = """
        MERGE (a:Entity:Anomaly {key: $a_key})
        SET a.title=$title, a.severity=$severity,
            a.created_at = coalesce(a.created_at, datetime()),
            a.updated_at = datetime()

        MERGE (p:Entity:Product {key: $p_key})
        SET p.name=$product,
            p.created_at = coalesce(p.created_at, datetime()), p.updated_at = datetime()

        MERGE (b:Entity:Build {key: $b_key})
        SET b.name=$build, b.version=$build,
            b.created_at = coalesce(b.created_at, datetime()), b.updated_at = datetime()

        MERGE (c:Entity:Component {key: $c_key})
        SET c.name=$component,
            c.created_at = coalesce(c.created_at, datetime()), c.updated_at = datetime()

        MERGE (s:Entity:Symptom {key: $s_key})
        SET s.name=$symptom,
            s.created_at = coalesce(s.created_at, datetime()), s.updated_at = datetime()

        MERGE (p)-[:HAS_BUILD]->(b)
        MERGE (a)-[:OBSERVED_IN]->(b)
        MERGE (a)-[:AFFECTS]->(c)
        MERGE (a)-[:HAS_SYMPTOM]->(s)
        """
        self._run(cypher, {
            'a_key': a_key, 'p_key': p_key, 'b_key': b_key, 'c_key': c_key, 's_key': s_key,
            'title': title, 'severity': severity,
            'product': product, 'build': build,
            'component': component, 'symptom': symptom,
        })

    def upsert_testcase_row(self, row: Dict[str, str]) -> None:
        """Row keys: CaseID, Title, Module, Priority"""
        case_id = row.get('CaseID') or ''
        if not case_id:
            return
        title = row.get('Title') or ''
        module_raw = row.get('Module') or ''
        priority = row.get('Priority') or ''

        comp = self.norm.norm_component(module_raw)
        t_key = self.norm.make_key('TestCase', case_id)
        c_key = self.norm.make_key('Component', comp)

        cypher = """
        MERGE (t:Entity:TestCase {key: $t_key})
        SET t.name=$title, t.priority=$priority,
            t.created_at = coalesce(t.created_at, datetime()), t.updated_at = datetime()

        MERGE (c:Entity:Component {key: $c_key})
        SET c.name=$component,
            c.created_at = coalesce(c.created_at, datetime()), c.updated_at = datetime()

        MERGE (t)-[:BELONGS_TO]->(c)
        """
        self._run(cypher, {
            't_key': t_key, 'c_key': c_key,
            'title': title, 'priority': priority,
            'component': comp,
        })

