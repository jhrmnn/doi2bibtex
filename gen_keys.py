#!/usr/bin/env python3
import bibtexparser as bibtex
import sys
from slugify import slugify
import hashlib
import re


bib = bibtex.load(sys.stdin)
for item in bib.entries:
    last = item['author'].split(' and ')[0].split()[-1]
    last = re.sub(r'[{}]', '', last)
    last_slg = slugify(last)
    last = ''.join([a.upper() if b.isupper() else a for a, b in zip(last_slg, last)])
    journal = slugify(''.join(w[0] for w in item['journal'].split())).upper()
    doihash = hashlib.sha1(item['doi'].lower().encode()).hexdigest()[-2:]
    year = item['year'][-2:]
    item['id'] = '{}{}{}_{}'.format(last, journal, year, doihash)
bibtex.dump(bib, sys.stdout)
