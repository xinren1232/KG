#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neo4j import GraphDatabase

URI='bolt://localhost:7687'
AUTH=('neo4j','password123')

DROP_MATCH = """
SHOW CONSTRAINTS YIELD name, entityType, labelsOrTypes, properties, type
WHERE any(l IN labelsOrTypes WHERE l='Term') AND properties = ['name']
RETURN name
"""

if __name__=='__main__':
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as s:
        # drop unique(name) on :Term if exists
        rows = s.run(DROP_MATCH).data()
        for r in rows:
            cname = r['name']
            if cname:
                s.run(f"DROP CONSTRAINT {cname} IF EXISTS")
                print('Dropped constraint:', cname)
        # create node key on (name, category)
        s.run("CREATE CONSTRAINT term_name_category_node_key IF NOT EXISTS FOR (t:Term) REQUIRE (t.name, t.category) IS NODE KEY")
        print('Ensured NODE KEY constraint on (:Term)(name,category)')
    driver.close()

