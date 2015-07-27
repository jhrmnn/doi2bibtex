#!/usr/bin/env python3
import bibtexparser as bibtex
import sys


allowed_keys = [
    'doi', 'url', 'year', 'volume', 'number', 'pages',
    'author', 'title', 'journal', 'id', 'type'
]

bib = bibtex.load(sys.stdin)
for item in bib.entries:
    if 'journaltitle' in item and 'journal' not in item:
        item['journal'] = item['journaltitle']
    authors = item['author'].split(' and ')
    authors = [a if ',' not in a else ' '.join(reversed(a.split(', '))) for a in authors]
    item['author'] = ' and '.join(authors)
    if 'date' in item and 'year' not in item:
        item['year'] = item['date'].split('-')[0]
    if 'doi' in item:
        item['url'] = 'http://dx.doi.org/{}'.format(item['doi'])
    for k in list(item):
        if k not in allowed_keys:
            del item[k]
bibtex.dump(bib, sys.stdout)
