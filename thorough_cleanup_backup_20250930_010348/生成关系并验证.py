#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从现有 Dictionary 节点属性（category/tags/aliases/term）生成关系，并验证结果：
- (:Dictionary)-[:HAS_TAG]->(:Tag)
- (:Dictionary)-[:IN_CATEGORY]->(:Category)
- (:Dictionary)-[:HAS_ALIAS]->(:Alias)
- (:Dictionary)-[:SAME_AS]->(:Dictionary)
脚本是幂等的（MERGE），可反复执行。
"""
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "password123"


def run(tx, query, **params):
    return tx.run(query, **params)


def exec_write(session, query):
    session.execute_write(lambda tx: run(tx, query))


def fetch_single(session, query):
    rec = session.execute_read(lambda tx: run(tx, query).single())
    return rec


def main():
    print("🚀 从属性生成关系并验证…")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        # 0) 基线信息
        total = fetch_single(session, "MATCH (d:Dictionary) RETURN count(d) AS c")["c"]
        print(f"📊 Dictionary 节点: {total}")

        # 1) 约束 / 索引
        print("\n🧩 创建约束/索引（如已存在将跳过）…")
        exec_write(session, """
        CREATE CONSTRAINT dict_term_unique IF NOT EXISTS
        FOR (d:Dictionary) REQUIRE d.term IS UNIQUE;
        """)
        exec_write(session, """
        CREATE CONSTRAINT tag_name_unique IF NOT EXISTS
        FOR (t:Tag) REQUIRE t.name IS UNIQUE;
        """)
        exec_write(session, """
        CREATE CONSTRAINT cat_name_unique IF NOT EXISTS
        FOR (c:Category) REQUIRE c.name IS UNIQUE;
        """)
        exec_write(session, """
        CREATE CONSTRAINT alias_name_unique IF NOT EXISTS
        FOR (a:Alias) REQUIRE a.name IS UNIQUE;
        """)
        print("✅ 约束/索引已确保存在")

        # 2) 物化多标签
        print("\n🏷️ 物化多标签 → HAS_TAG …")
        exec_write(session, """
        MATCH (d:Dictionary) WHERE d.tags IS NOT NULL AND size(d.tags) > 0
        UNWIND d.tags AS tag
        WITH d, trim(toString(tag)) AS t WHERE t <> ''
        MERGE (tg:Tag {name: t})
        MERGE (d)-[:HAS_TAG]->(tg);
        """)
        tag_nodes = fetch_single(session, "MATCH (t:Tag) RETURN count(t) AS c")["c"]
        tag_rels = fetch_single(session, "MATCH ()-[r:HAS_TAG]->() RETURN count(r) AS c")["c"]
        print(f"   ▶ Tag 节点: {tag_nodes}，HAS_TAG 关系: {tag_rels}")

        # 3) 物化类别
        print("\n📁 物化类别 → IN_CATEGORY …")
        exec_write(session, """
        MATCH (d:Dictionary) WHERE d.category IS NOT NULL AND trim(d.category) <> ''
        MERGE (c:Category {name: d.category})
        MERGE (d)-[:IN_CATEGORY]->(c);
        """)
        cat_nodes = fetch_single(session, "MATCH (c:Category) RETURN count(c) AS c")["c"]
        cat_rels = fetch_single(session, "MATCH ()-[r:IN_CATEGORY]->() RETURN count(r) AS c")["c"]
        print(f"   ▶ Category 节点: {cat_nodes}，IN_CATEGORY 关系: {cat_rels}")

        # 4) 物化别名
        print("\n🔁 物化别名 → HAS_ALIAS, SAME_AS …")
        exec_write(session, """
        MATCH (d:Dictionary) WHERE d.aliases IS NOT NULL AND size(d.aliases) > 0
        UNWIND d.aliases AS al
        WITH d, trim(toString(al)) AS a WHERE a <> '' AND a <> d.term
        MERGE (al:Alias {name: a})
        MERGE (d)-[:HAS_ALIAS]->(al);
        """)
        alias_nodes = fetch_single(session, "MATCH (a:Alias) RETURN count(a) AS c")["c"]
        alias_rels = fetch_single(session, "MATCH ()-[r:HAS_ALIAS]->() RETURN count(r) AS c")["c"]
        print(f"   ▶ Alias 节点: {alias_nodes}，HAS_ALIAS 关系: {alias_rels}")

        # SAME_AS：当别名命中另一条术语
        exec_write(session, """
        MATCH (d1:Dictionary) WHERE d1.aliases IS NOT NULL AND size(d1.aliases) > 0
        UNWIND d1.aliases AS al
        WITH d1, trim(toString(al)) AS a WHERE a <> ''
        MATCH (d2:Dictionary {term: a})
        WITH DISTINCT d1, d2 WHERE id(d1) < id(d2)
        MERGE (d1)-[:SAME_AS]->(d2);
        """)
        same_as_cnt = fetch_single(session, "MATCH ()-[r:SAME_AS]->() RETURN count(r) AS c")["c"]
        print(f"   ▶ SAME_AS 关系: {same_as_cnt}")

        # 5) 汇总
        print("\n✅ 执行完成，关系统计：")
        rows = session.execute_read(lambda tx: run(tx, """
            CALL {
              MATCH ()-[r:HAS_TAG]->() RETURN 'HAS_TAG' AS type, count(r) AS cnt
            }
            UNION ALL CALL {
              MATCH ()-[r:IN_CATEGORY]->() RETURN 'IN_CATEGORY' AS type, count(r) AS cnt
            }
            UNION ALL CALL {
              MATCH ()-[r:HAS_ALIAS]->() RETURN 'HAS_ALIAS' AS type, count(r) AS cnt
            }
            UNION ALL CALL {
              MATCH ()-[r:SAME_AS]->() RETURN 'SAME_AS' AS type, count(r) AS cnt
            }
        """))
        for r in rows:
            print(f"   - {r['type']}: {r['cnt']}")

        # 6) 验证 Relationships 总数
        total_rels = fetch_single(session, "MATCH ()-[r]->() RETURN count(r) AS c")["c"]
        print(f"\n📈 当前关系总数: {total_rels}")

    driver.close()
    print("\n🎉 全部完成。可在 Neo4j 浏览器刷新查看关系类型与数量。")


if __name__ == "__main__":
    main()

