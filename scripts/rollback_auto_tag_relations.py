#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neo4j import GraphDatabase
from datetime import datetime

URI = 'bolt://localhost:7687'
AUTH = ('neo4j', 'password123')

BID = f"auto-tag-relations-{datetime.utcnow().strftime('%Y%m%d')}"

if __name__ == '__main__':
    print('Rolling back RELATED_TO edges with build_id =', BID)
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as s:
        c1 = s.run('MATCH ()-[r:RELATED_TO]->() WHERE r.build_id=$bid RETURN count(r) AS c', bid=BID).single()['c']
        print('Edges to delete:', c1)
        c2 = s.run('MATCH ()-[r:RELATED_TO]->() WHERE r.build_id=$bid DELETE r RETURN count(r) AS c', bid=BID).single()['c']
        print('Deleted edges:', c2)
    driver.close()

