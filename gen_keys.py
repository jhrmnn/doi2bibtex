#!/usr/bin/env python3
import bibtexparser as bibtex
import sys
from slugify import slugify
import hashlib
import re


bib = bibtex.load(sys.stdin)
for item in bib.entries:
    author = item['author'].split(' and ')[0]
    if ',' in author:
        last = author.split(',')[0].strip()
    else:
        last = author.split()[-1]
    last = re.sub(r'[{}]', '', last)
    last_slg = slugify(last)
    last = ''.join([a.upper() if b.isupper() else a
                    for a, b in zip(last_slg, last)])
    journal = slugify(''.join(w[0] for w in item['journal'].split())).upper()
    year = item.get('year', item['date'].split('-')[0])
    year = year[-2:]
    doihash = hashlib.sha1(item['doi'].lower().encode()).hexdigest()[-2:]
    item['id'] = '{}{}{}*{}'.format(last, journal, year, doihash)
bibtex.dump(bib, sys.stdout)
