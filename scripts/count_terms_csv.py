#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv, collections
rows=list(csv.DictReader(open('data/dictionary/dictionary_v1.csv',encoding='utf-8')))
terms=set()
pairs=set()
bycat=collections.Counter()
for r in rows:
    t=r['term'].strip()
    c=r['category'].strip()
    terms.add(t)
    pairs.add((t,c))
    bycat[c]+=1
print('CSV rows:', len(rows))
print('Distinct terms:', len(terms))
print('Distinct (term,category):', len(pairs))
print('By category (rows):', dict(bycat))

