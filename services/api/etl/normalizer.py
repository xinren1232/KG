#!/usr/bin/env python3
"""
Normalization utilities using vocab tables and ontology key rules.
- Map component aliases to standard names
- Generate keys: Product:xxx, Build:yyy, Component:stdName, Symptom:stdName, Anomaly:<ID>
- Clean severity text, trim whitespaces
"""
from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd

class Vocab:
    def __init__(self, root: Path|None=None):
        root = root or Path('.')
        self.comp_alias2std: Dict[str,str] = {}
        self.symptom_std: set[str] = set()
        self.cause_std: set[str] = set()
        self._load(root)
    def _load(self, root: Path):
        try:
            df = pd.read_csv(root/ 'data/vocab/components.csv')
            for _, r in df.iterrows():
                name = str(r.get('name','')).strip()
                alias = str(r.get('alias','')).strip()
                if name:
                    self.comp_alias2std[name.lower()] = name
                if alias:
                    self.comp_alias2std[alias.lower()] = name or alias
        except Exception:
            pass
        try:
            df = pd.read_csv(root/ 'data/vocab/symptoms.csv')
            for v in df['name'].dropna().tolist():
                self.symptom_std.add(str(v).strip())
        except Exception:
            pass
        try:
            df = pd.read_csv(root/ 'data/vocab/causes.csv')
            for v in df['name'].dropna().tolist():
                self.cause_std.add(str(v).strip())
        except Exception:
            pass


def std_component(vocab: Vocab, name: str) -> str:
    n = (name or '').strip()
    if not n:
        return n
    return vocab.comp_alias2std.get(n.lower(), n)


def std_symptom(vocab: Vocab, name: str) -> str:
    n = (name or '').strip()
    if not n:
        return n
    for s in vocab.symptom_std:
        if s.lower() == n.lower():
            return s
    return n


def make_key(label: str, name: str, extra: Dict|None=None) -> str:
    extra = extra or {}
    if label in {'Product','Component','Symptom'}:
        return f"{label}:{name}"
    if label == 'Build':
        return f"Build:{name}"
    if label == 'Anomaly':
        # prefer explicit ID; else fallback to title hash
        aid = extra.get('anomalyid') or name
        return f"Anomaly:{aid}"
    return f"{label}:{name}"


def normalize_anomaly_rows(rows: List[Dict], vocab: Vocab) -> List[Dict]:
    out: List[Dict] = []
    for r in rows:
        anomalyid = (r.get('anomalyid') or '').strip()
        title = (r.get('title') or '').strip()
        severity = (r.get('severity') or '').strip()
        product = (r.get('product') or '').strip()
        build = (r.get('build') or '').strip()
        component = std_component(vocab, r.get('component') or '')
        symptom = std_symptom(vocab, r.get('symptom') or '')
        if not (anomalyid or title):
            continue
        # keys
        pkey = make_key('Product', product or 'Unknown')
        bkey = make_key('Build', build or 'Unknown')
        ckey = make_key('Component', component or 'Unknown')
        skey = make_key('Symptom', symptom or 'Unknown')
        akey = make_key('Anomaly', anomalyid or title, {'anomalyid': anomalyid})
        out.append({
            'anomaly': {'key': akey, 'title': title, 'severity': severity},
            'product': {'key': pkey, 'name': product},
            'build': {'key': bkey, 'name': build},
            'component': {'key': ckey, 'name': component},
            'symptom': {'key': skey, 'name': symptom},
        })
    return out


def normalize_case_rows(rows: List[Dict], vocab: Vocab) -> List[Dict]:
    out: List[Dict] = []
    for r in rows:
        cid = (r.get('caseid') or '').strip()
        title = (r.get('title') or '').strip()
        module = std_component(vocab, r.get('module') or '')
        priority = (r.get('priority') or '').strip()
        if not (cid or title):
            continue
        out.append({
            'testcase': {
                'key': f"TestCase:{cid or title}",
                'title': title, 'priority': priority
            },
            'component': {'key': make_key('Component', module or 'Unknown'), 'name': module}
        })
    return out

