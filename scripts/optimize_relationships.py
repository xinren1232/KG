#!/usr/bin/env python3
"""
Graph Relationship Optimizer for Neo4j

Goals:
- Normalize relationship taxonomy (migrate USES_MATERIAL -> CONSUMES)
- Deduplicate relationships between the same pair and type (keep highest confidence)
- Canonicalize RELATED_TO as single-direction (keep a->b where elementId(a) < elementId(b))
- Prune low-confidence inferred edges (confidence < threshold)
- Optionally cap RELATED_TO to Top-K per node by confidence

Default mode is dry-run: compute and print impact without modifying data.

Usage examples:
  python scripts/optimize_relationships.py --dry-run
  python scripts/optimize_relationships.py --apply --threshold 0.35 --topk-related-to 10

Environment variables:
  NEO4J_URI (default bolt://localhost:7687)
  NEO4J_USER (default neo4j)
  NEO4J_PASS (default password123)
"""
import os
import sys
import argparse
from dataclasses import dataclass
from typing import Optional
from neo4j import GraphDatabase

@dataclass
class Config:
    uri: str
    user: str
    password: str
    threshold: float = 0.3
    topk_related_to: Optional[int] = None
    apply: bool = False
    do_migrate_uses_material: bool = True
    do_dedup: bool = True
    do_canonical_related_to: bool = True
    do_prune_low_conf: bool = True
    do_topk_related_to: bool = False


def get_driver():
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    pw = os.getenv("NEO4J_PASS", "password123")
    return GraphDatabase.driver(uri, auth=(user, pw)), uri, user


def count_total_rels(tx):
    return tx.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]


def run():
    parser = argparse.ArgumentParser(description="Optimize Neo4j relationships")
    parser.add_argument("--threshold", type=float, default=0.3, help="confidence threshold for pruning")
    parser.add_argument("--topk-related-to", type=int, default=None, help="Top-K cap per node for RELATED_TO (by confidence)")
    parser.add_argument("--apply", action="store_true", help="apply changes (default dry-run)")
    parser.add_argument("--skip-migrate-uses-material", action="store_true")
    parser.add_argument("--skip-dedup", action="store_true")
    parser.add_argument("--skip-canonical-related-to", action="store_true")
    parser.add_argument("--skip-prune", action="store_true")
    parser.add_argument("--enable-topk-related-to", action="store_true")

    args = parser.parse_args()
    cfg = Config(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASS", "password123"),
        threshold=args.threshold,
        topk_related_to=args.topk_related_to,
        apply=args.apply,
        do_migrate_uses_material=not args.skip_migrate_uses_material,
        do_dedup=not args.skip_dedup,
        do_canonical_related_to=not args.skip_canonical_related_to,
        do_prune_low_conf=not args.skip_prune,
        do_topk_related_to=args.enable_topk_related_to and args.topk_related_to is not None,
    )

    driver, uri, user = get_driver()
    print(f"Connecting to {uri} as {user} ...")
    with driver.session() as session:
        before = session.execute_read(count_total_rels)
        print(f"Total relationships (before): {before}")

        # 1) Migrate USES_MATERIAL -> CONSUMES
        if cfg.do_migrate_uses_material:
            mig_counts = session.run(
                """
                // pairs that will be migrated
                MATCH (p)-[r:USES_MATERIAL]->(m)
                WITH p,m, count(r) AS c
                RETURN count(*) AS rel_pairs, sum(c) AS rels
                """
            ).single()
            rel_pairs = mig_counts["rel_pairs"] if mig_counts else 0
            rels = mig_counts["rels"] if mig_counts else 0
            print(f"USES_MATERIAL present: pairs={rel_pairs}, rels={rels}")

            # potential duplicates when migrating (where CONSUMES already exists)
            dup_pairs = session.run(
                """
                MATCH (p)-[:USES_MATERIAL]->(m)
                MATCH (p)-[:CONSUMES]->(m)
                RETURN count(*) AS dup_pairs
                """
            ).single()["dup_pairs"]
            print(f"Potential CONSUMES duplicates after migration: {dup_pairs}")

            if cfg.apply and rels:
                session.run(
                    """
                    MATCH (p)-[r:USES_MATERIAL]->(m)
                    MERGE (p)-[c:CONSUMES]->(m)
                    SET c += properties(r), c.migrated_from = 'USES_MATERIAL', c.migrated_at = datetime()
                    WITH r
                    DELETE r
                    """
                )
                print(f"Migrated {rels} USES_MATERIAL -> CONSUMES and deleted source rels")

        # 2) Deduplicate (keep highest confidence per a,b,type)
        if cfg.do_dedup:
            dups = session.run(
                """
                MATCH (a)-[r]->(b)
                WITH elementId(a) AS aId, elementId(b) AS bId, type(r) AS t, collect(r) AS rels,
                     size(collect(r)) AS c
                WHERE c > 1
                RETURN count(*) AS pairs_with_dups, sum(c-1) AS duplicate_rels
                """
            ).single()
            print(f"Duplicate pairs: {dups['pairs_with_dups']}, redundant rels: {dups['duplicate_rels']}")

            if cfg.apply and (dups["duplicate_rels"] or 0) > 0:
                # Execute per type to avoid memory blowups
                types = session.run("MATCH ()-[r]->() RETURN DISTINCT type(r) AS t").data()
                for trow in types:
                    t = trow['t']
                    session.run(
                        f"""
                        MATCH (a)-[r:{t}]->(b)
                        WITH a,b, r, coalesce(r.confidence,0) AS c
                        ORDER BY c DESC
                        WITH a,b, collect(r) AS rels
                        WITH rels[0] AS keep, rels[1..] AS dels
                        FOREACH (x IN dels | DELETE x)
                        """
                    )
                print("Deduplication completed (kept highest confidence per pair/type)")

        # 3) Canonicalize RELATED_TO: keep only a->b where elementId(a) < elementId(b)
        if cfg.do_canonical_related_to:
            bidir = session.run(
                """
                MATCH (a)-[:RELATED_TO]->(b)
                WHERE (b)-[:RELATED_TO]->(a) AND elementId(a) < elementId(b)
                RETURN count(*) AS bidirectional_pairs
                """
            ).single()["bidirectional_pairs"]
            print(f"RELATED_TO bidirectional pairs: {bidir}")

            if cfg.apply and bidir:
                session.run(
                    """
                    MATCH (a)-[r:RELATED_TO]->(b)
                    WHERE (b)-[:RELATED_TO]->(a) AND elementId(a) > elementId(b)
                    DELETE r
                    """
                )
                print("Canonicalized RELATED_TO (removed reverse duplicates)")

        # 4) Prune low-confidence inferred edges
        if cfg.do_prune_low_conf:
            low_conf = session.run(
                """
                MATCH ()-[r]->()
                WHERE coalesce(r.inferred, true) = true AND coalesce(r.confidence, 0.0) < $thr
                RETURN count(r) AS to_delete
                """,
                thr=cfg.threshold,
            ).single()["to_delete"]
            print(f"Low-confidence inferred relationships (< {cfg.threshold}): {low_conf}")

            if cfg.apply and low_conf:
                session.run(
                    """
                    MATCH ()-[r]->()
                    WHERE coalesce(r.inferred, true) = true AND coalesce(r.confidence, 0.0) < $thr
                    DELETE r
                    """,
                    thr=cfg.threshold,
                )
                print("Pruned low-confidence inferred relationships")

        # 5) Top-K per node for RELATED_TO (by confidence)
        if cfg.do_topk_related_to and cfg.topk_related_to is not None:
            more_than_k = session.run(
                """
                MATCH (n)-[r:RELATED_TO]->(m)
                WITH n, r ORDER BY coalesce(r.confidence,0) DESC
                WITH n, collect(r) AS rels
                WITH n, CASE WHEN size(rels) > $k THEN size(rels) - $k ELSE 0 END AS to_del
                RETURN sum(to_del) AS deletions
                """,
                k=cfg.topk_related_to,
            ).single()["deletions"]
            print(f"Top-K RELATED_TO planned deletions (K={cfg.topk_related_to}): {more_than_k}")

            if cfg.apply and more_than_k:
                session.run(
                    """
                    MATCH (n)-[r:RELATED_TO]->(m)
                    WITH n, r ORDER BY coalesce(r.confidence,0) DESC
                    WITH n, collect(r) AS rels
                    WITH n, rels[$k..] AS dels
                    FOREACH (x IN dels | DELETE x)
                    """,
                    k=cfg.topk_related_to,
                )
                print("Applied Top-K cap for RELATED_TO")

        after = session.execute_read(count_total_rels)
        print(f"Total relationships (after): {after} (dry-run will show same as before)")

        if not cfg.apply:
            print("Dry-run complete. Re-run with --apply to execute changes.")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("Optimization failed:", e)
        sys.exit(1)

