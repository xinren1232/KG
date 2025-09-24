#!/usr/bin/env python3
"""
Parse Excel sources for ETL
- anomalies.xlsx: AnomalyID, Title, Severity, Product, Build, Component, Symptom
- testcases.xlsx: CaseID, Title, Module, Priority
Note: Use pandas with openpyxl engine under the hood.
"""
from __future__ import annotations
import pandas as pd
from typing import List, Dict, Tuple
from pathlib import Path

CANON_ANOMALY = {
    'anomalyid': 'AnomalyID',
    'anomaly_id': 'AnomalyID',
    'id': 'AnomalyID',
    'title': 'Title',
    'severity': 'Severity',
    'product': 'Product',
    'build': 'Build',
    'component': 'Component',
    'module': 'Component',
    'symptom': 'Symptom',
}

CANON_CASE = {
    'caseid': 'CaseID',
    'case_id': 'CaseID',
    'id': 'CaseID',
    'title': 'Title',
    'module': 'Module',
    'component': 'Module',
    'priority': 'Priority',
}

def _canonize_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    rename = {}
    for c in df.columns:
        key = str(c).strip().lower().replace(' ', '').replace('_', '')
        if key in mapping:
            rename[c] = mapping[key]
    return df.rename(columns=rename)


def read_anomalies(path: str | Path) -> List[Dict[str, str]]:
    p = Path(path)
    if not p.exists():
        return []
    df = pd.read_excel(p, engine='openpyxl')
    df = _canonize_columns(df, CANON_ANOMALY)
    # keep only expected columns
    cols = ['AnomalyID','Title','Severity','Product','Build','Component','Symptom']
    for col in cols:
        if col not in df.columns:
            df[col] = None
    df = df[cols]
    records = []
    for _, r in df.iterrows():
        rec = {c: ('' if pd.isna(r[c]) else str(r[c]).strip()) for c in cols}
        # minimal required: AnomalyID, Product, Build, Component
        if rec['AnomalyID']:
            records.append(rec)
    return records


def read_testcases(path: str | Path) -> List[Dict[str, str]]:
    p = Path(path)
    if not p.exists():
        return []
    df = pd.read_excel(p, engine='openpyxl')
    df = _canonize_columns(df, CANON_CASE)
    cols = ['CaseID','Title','Module','Priority']
    for col in cols:
        if col not in df.columns:
            df[col] = None
    df = df[cols]
    records = []
    for _, r in df.iterrows():
        rec = {c: ('' if pd.isna(r[c]) else str(r[c]).strip()) for c in cols}
        if rec['CaseID']:
            records.append(rec)
    return records

