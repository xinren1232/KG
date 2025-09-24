#!/usr/bin/env python3
"""
Batch ETL runner
- Input: folder or files (Excel: anomalies.xlsx, testcases.xlsx)
- Steps: parse -> normalize -> upsert to Neo4j

Usage examples:
  python services/api/etl/run_batch.py --in data/import
  python services/api/etl/run_batch.py --anomalies d:/KG/data/anomalies.xlsx --testcases d:/KG/data/testcases.xlsx 

Docker example (as per design):
  docker exec -it kg_etl python /app/etl/run_batch.py --in /app/data
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import List
from parse_excel import parse_anomalies_excel, parse_testcases_excel, detect_and_parse
from normalizer import Vocab, normalize_anomaly_rows, normalize_case_rows
from upsert_writer import Neo4jUpserter


def find_inputs(in_dir: Path) -> List[Path]:
    files: List[Path] = []
    for p in in_dir.glob('*.xlsx'):
        files.append(p)
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='in_dir', type=str, help='input folder containing excel files')
    ap.add_argument('--anomalies', type=str, help='explicit anomalies.xlsx file path')
    ap.add_argument('--testcases', type=str, help='explicit testcases.xlsx file path')
    ap.add_argument('--neo4j-uri', type=str, default='bolt://localhost:7687')
    ap.add_argument('--neo4j-user', type=str, default='neo4j')
    ap.add_argument('--neo4j-password', type=str, default='password')
    args = ap.parse_args()

    vocab = Vocab(Path('.'))
    upserter = Neo4jUpserter(uri=args.neo4j_uri, user=args.neo4j_user, password=args.neo4j_password)

    try:
        # Collect inputs
        anomalies_rows = []
        cases_rows = []
        if args.anomalies:
            anomalies_rows = parse_anomalies_excel(args.anomalies)
        if args.testcases:
            cases_rows = parse_testcases_excel(args.testcases)
        if args.in_dir and (not anomalies_rows or not cases_rows):
            for p in find_inputs(Path(args.in_dir)):
                kind, _ = detect_and_parse(p)
                if kind == 'anomalies' and not anomalies_rows:
                    anomalies_rows = parse_anomalies_excel(p)
                elif kind == 'testcases' and not cases_rows:
                    cases_rows = parse_testcases_excel(p)

        # Normalize
        an_records = normalize_anomaly_rows(anomalies_rows, vocab) if anomalies_rows else []
        tc_records = normalize_case_rows(cases_rows, vocab) if cases_rows else []

        # Upsert
        for rec in an_records:
            upserter.upsert_anomaly_bundle(rec)
        for rec in tc_records:
            upserter.upsert_testcase_bundle(rec)

        print(f"ETL Done. anomalies={len(an_records)}, testcases={len(tc_records)}")
    finally:
        upserter.close()


if __name__ == '__main__':
    main()

