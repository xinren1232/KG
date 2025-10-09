#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将现有 Tag 归入业务模块 Module，并将 Dictionary 直连到 Module。
规则：当 Dictionary 的任一 Tag 属于 module_whitelist，则：
  (tg:Tag)-[:IN_MODULE]->(m:Module)
  (d:Dictionary)-[:IN_MODULE]->(m:Module)
脚本为幂等（MERGE）。
"""
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "password123"

module_whitelist = [
    '显示相关','影像相关','电池','PCB','射频相关','声学','人机交互','热管理','半导体','可靠性',
    '设计','测试验证','安全相关','SMT','CMF','注塑','充电','点胶','封装','EMC','FPC','包装',
    '外观','结构相关','电气连接','电气性能','硬件相关','传感器','时钟'
]

cypher_prepare = """
UNWIND $mods AS name
MERGE (:Module {name: name});
"""

cypher_tag_to_module = """
MATCH (tg:Tag)
WHERE tg.name IN $mods
MATCH (m:Module {name: tg.name})
MERGE (tg)-[:IN_MODULE]->(m);
"""

cypher_dict_to_module = """
MATCH (d:Dictionary)-[:HAS_TAG]->(tg:Tag)
WHERE tg.name IN $mods
MATCH (m:Module {name: tg.name})
MERGE (d)-[:IN_MODULE]->(m);
"""

cypher_stats = """
CALL {
  MATCH (m:Module) RETURN count(m) AS modules
}
CALL {
  MATCH (:Tag)-[r:IN_MODULE]->(:Module) RETURN count(r) AS t2m
}
CALL {
  MATCH (:Dictionary)-[r:IN_MODULE]->(:Module) RETURN count(r) AS d2m
}
RETURN modules, t2m, d2m;
"""

def main():
    print("🧭 建立模块分组并联接…")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        session.execute_write(lambda tx: tx.run(cypher_prepare, mods=module_whitelist))
        session.execute_write(lambda tx: tx.run(cypher_tag_to_module, mods=module_whitelist))
        session.execute_write(lambda tx: tx.run(cypher_dict_to_module, mods=module_whitelist))
        rec = session.execute_read(lambda tx: tx.run(cypher_stats).single())
        print(f"📊 Module 节点: {rec['modules']}")
        print(f"📊 Tag→Module 关系: {rec['t2m']}")
        print(f"📊 Dictionary→Module 关系: {rec['d2m']}")
    driver.close()
    print("✅ 完成。可在浏览器用 MATCH (m:Module) RETURN m; 查看模块。")

if __name__ == "__main__":
    main()

