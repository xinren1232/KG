#!/usr/bin/env python3
"""
Normalizer for Quality KG ETL
- Component alias mapping using data/vocab/components.csv
- Symptom/RootCause vocab normalization using data/vocab/symptoms.csv, data/vocab/causes.csv
- Unified key generation according to ontology_v0.1.md
"""
from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Dict, Optional

class Normalizer:
    def __init__(self):
        self.comp_alias2std: Dict[str, str] = {}
        self.symptom_std: Dict[str, str] = {}
        self.cause_std: Dict[str, str] = {}
        self._load_vocabs()

    def _load_vocabs(self) -> None:
        # components.csv: name,alias
        comp_path = Path('data/vocab/components.csv')
        if comp_path.exists():
            df = pd.read_csv(comp_path)
            for _, r in df.iterrows():
                name = str(r.get('name', '')).strip()
                alias = str(r.get('alias', '')).strip()
                if name:
                    self.comp_alias2std[name.lower()] = name
                if alias:
                    self.comp_alias2std[alias.lower()] = name or alias
        # symptoms.csv: name
        sym_path = Path('data/vocab/symptoms.csv')
        if sym_path.exists():
            df = pd.read_csv(sym_path)
            for x in df['name'].dropna().tolist():
                s = str(x).strip()
                self.symptom_std[s.lower()] = s
        # causes.csv: name
        cause_path = Path('data/vocab/causes.csv')
        if cause_path.exists():
            df = pd.read_csv(cause_path)
            for x in df['name'].dropna().tolist():
                s = str(x).strip()
                self.cause_std[s.lower()] = s

    @staticmethod
    def _clean(s: Optional[str]) -> str:
        if s is None:
            return ''
        return str(s).strip()

    def norm_component(self, name: Optional[str]) -> str:
        n = self._clean(name)
        return self.comp_alias2std.get(n.lower(), n)

    def norm_symptom(self, name: Optional[str]) -> str:
        n = self._clean(name)
        return self.symptom_std.get(n.lower(), n)

    def make_key(self, label: str, name: str, extra: Optional[Dict[str, str]] = None) -> str:
        extra = extra or {}
        if label in ('Product','Component','Owner','Supplier','Doc','Symptom','RootCause','Countermeasure'):
            return f"{label}:{name}"
        if label == 'Build':
            return f"Build:{extra.get('version', name)}"
        if label == 'TestCase':
            return f"TestCase:{name}"
        if label == 'TestStep':
            cid = extra.get('case_id', name)
            idx = extra.get('index', '')
            return f"TestStep:{cid}-{idx}".rstrip('-')
        if label == 'TestResult':
            suffix = extra.get('build') or extra.get('version') or ''
            return f"TestResult:{name}-{suffix}".rstrip('-')
        if label == 'Anomaly':
            return f"Anomaly:{extra.get('code', name)}"
        return f"{label}:{name}"

