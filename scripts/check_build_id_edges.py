#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neo4j import GraphDatabase

URI='bolt://localhost:7687'
AUTH=('neo4j','password123')
BID='auto-tag-relations-20250928'

if __name__=='__main__':
    driver=GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as s:
        c = s.run('MATCH ()-[r:RELATED_TO]->() WHERE r.build_id=$bid RETURN count(r) AS c', bid=BID).single()['c']
        print('Remaining edges with build_id', BID, ':', c)
    driver.close()

