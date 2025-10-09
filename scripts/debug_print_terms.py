#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neo4j import GraphDatabase

d=GraphDatabase.driver('bolt://localhost:7687',auth=('neo4j','password123'))
with d.session() as s:
    data = s.run('MATCH (t:Term) RETURN t.name AS n, t.category AS c LIMIT 10').data()
    print('Sample Terms:', data)
    comp = s.run("MATCH (t:Term {name:$name}) RETURN t.name AS n, t.category AS c", name='BTB连接器').data()
    print('BTB连接器:', comp)
    counts = s.run('MATCH (t:Term) RETURN labels(t) AS labels, t.category AS c, count(*) AS cnt ORDER BY cnt DESC').data()
    print('Counts by category:', counts)

d.close()

