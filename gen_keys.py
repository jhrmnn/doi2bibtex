#!/usr/bin/env python3
import bibtexparser as bibtex
import sys
from slugify import slugify
import hashlib


bib = bibtex.load(sys.stdin)
for item in bib.entries:
    last = item['author'].split(' and ')[0].split()[-1]
    last_slg = slugify(last)
    last = ''.join([a.upper() if b.isupper() else a
                    for a, b in zip(last_slg, last)])
    journal = slugify(''.join(w[0] for w in item['journal'].split())).upper()
    year = item['year'][-2:]
    doihash = hashlib.sha1(item['doi'].encode()).hexdigest()[-2:]
    item['id'] = '{}{}{}.{}'.format(last, journal, year, doihash)
bibtex.dump(bib, sys.stdout)
