#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neo4j import GraphDatabase

URI='bolt://localhost:7687'
AUTH=('neo4j','password123')

if __name__=='__main__':
    driver=GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as s:
        # 删除 Alias 与 Term（会自动删除关联 SAME_AS/BELONGS_TO/HAS_TAG/ALIAS_OF 等边）
        c1 = s.run('MATCH (a:Alias) RETURN count(a) AS c').single()['c']
        c2 = s.run('MATCH (t:Term) RETURN count(t) AS c').single()['c']
        print('Before delete: Alias=', c1, ' Term=', c2)
        s.run('MATCH (a:Alias) DETACH DELETE a')
        s.run('MATCH (t:Term) DETACH DELETE t')
        c1b = s.run('MATCH (a:Alias) RETURN count(a) AS c').single()['c']
        c2b = s.run('MATCH (t:Term) RETURN count(t) AS c').single()['c']
        print('After delete: Alias=', c1b, ' Term=', c2b)
    driver.close()

