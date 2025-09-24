#!/usr/bin/env python3
"""
Parse Excel inputs for ETL → Graph.
- anomalies.xlsx: AnomalyID, Title, Severity, Product, Build, Component, Symptom
- testcases.xlsx: CaseID, Title, Module, Priority

Implementation notes:
- Use pandas + openpyxl engine for robustness
- Column header normalization: strip, lower, remove spaces, standardize aliases
- Return list[dict] per row, skipping empty rows
"""
from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple

EXPECTED_ANOMALY_COLS = [
    'anomalyid','title','severity','product','build','component','symptom'
]
EXPECTED_CASE_COLS = [
    'caseid','title','module','priority'
]

ALIASES_MAP = {
    # anomalies
    'anomaly id':'anomalyid','anomaly_id':'anomalyid','bugid':'anomalyid','缺陷编号':'anomalyid','异常编号':'anomalyid','追踪号':'anomalyid',
    'summary':'title','问题标题':'title','标题':'title',
    '严重程度':'severity','级别':'severity','priority':'severity','优先级':'severity',
    '产品':'product','机型':'product','型号':'product','product name':'product','productname':'product',
    '版本':'build','build version':'build','buildversion':'build','软件版本':'build',
    '组件':'component','模块':'component','module':'component','子系统':'component',
    '症状':'symptom','现象':'symptom',
    # cases
    'case id':'caseid','用例编号':'caseid','测试用例编号':'caseid','id':'caseid',
    '用例标题':'title','名称':'title','用例名称':'title',
    '模块(组件)':'module','模块名':'module','component':'module','子模块':'module',
}


def _normalize_columns(cols: List[str]) -> List[str]:
    def norm(c: str) -> str:
        c = (c or '').strip()
        c = c.replace('\u3000',' ').replace('\t',' ').replace('\n',' ')
        c = c.replace('：',':').replace('（','(').replace('）',')')
        c = ''.join(ch for ch in c if ch not in ' /\\-_')
        c_low = c.lower()
        return ALIASES_MAP.get(c_low, c_low)
    return [norm(c) for c in cols]


def _read_excel(path: Path, sheet: str|int|None=None) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet, engine='openpyxl')


def parse_anomalies_excel(path: str|Path) -> List[Dict]:
    p = Path(path)
    df = _read_excel(p)
    df.columns = _normalize_columns([str(c) for c in df.columns])
    # retain only expected cols if present; missing cols will be filled with ''
    for col in EXPECTED_ANOMALY_COLS:
        if col not in df.columns:
            df[col] = ''
    rows: List[Dict] = []
    for _, r in df.iterrows():
        row = {k: ('' if pd.isna(r[k]) else str(r[k]).strip()) for k in EXPECTED_ANOMALY_COLS}
        # minimal validity: need anomalyid or title
        if any(row.values()):
            rows.append(row)
    return rows


def parse_testcases_excel(path: str|Path) -> List[Dict]:
    p = Path(path)
    df = _read_excel(p)
    df.columns = _normalize_columns([str(c) for c in df.columns])
    for col in EXPECTED_CASE_COLS:
        if col not in df.columns:
            df[col] = ''
    rows: List[Dict] = []
    for _, r in df.iterrows():
        row = {k: ('' if pd.isna(r[k]) else str(r[k]).strip()) for k in EXPECTED_CASE_COLS}
        if any(row.values()):
            rows.append(row)
    return rows


def detect_and_parse(path: str|Path) -> Tuple[str, List[Dict]]:
    """Best-effort detect file type by headers and return (kind, rows).
    kind in {'anomalies','testcases','unknown'}
    """
    p = Path(path)
    df = _read_excel(p)
    df.columns = _normalize_columns([str(c) for c in df.columns])
    cols = set(df.columns)
    if set(EXPECTED_ANOMALY_COLS[:3]).issubset(cols):
        return 'anomalies', parse_anomalies_excel(p)
    if set(EXPECTED_CASE_COLS[:2]).issubset(cols):
        return 'testcases', parse_testcases_excel(p)
    # fallback guess by Chinese names
    if {'异常编号','症状','产品'} & set(df.columns):
        return 'anomalies', parse_anomalies_excel(p)
    return 'unknown', []

