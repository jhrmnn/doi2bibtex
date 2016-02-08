#!/usr/bin/env python3
"""Generates bibtex citation keys.

Usage:
    gen_keys.py FILE
"""
from docopt import docopt
import bibtexparser as bibtex
import sys
from slugify import slugify
import re
from itertools import groupby


args = docopt(__doc__)

with open(args['FILE']) as f:
    old_bib = bibtex.load(f)
old_keys = {item['doi']: item['ID'] for item in old_bib.entries if 'doi' in item}

bib = bibtex.load(sys.stdin)
new_keys = []
for item in bib.entries:
    last = item['author'].split(' and ')[0].split(',')[0].strip()
    last = re.sub(r'[{}]', '', last)
    last_slg = slugify(last)
    last = ''.join([a.upper() if b.isupper() else a for a, b in zip(last_slg, last)])
    year = item['year'][-2:]
    if 'journal' in item:
        journal = slugify(''.join(w[0] for w in item['journal'].split())).upper()
        # doi = item.get('doi', '')
        # doihash = hashlib.sha1(doi.lower().encode()).hexdigest()[-2:]
        key = '{}{}{}'.format(last, journal, year)
    else:
        key = '{}{}'.format(last, year)
    item['ID'] = key
    new_keys.append(key)

entries = sorted(bib.entries, key=lambda x: x['ID'])
for key, group in groupby(entries, key=lambda x: x['ID']):
    group = list(group)
    if len(group) > 1:
        idx = 'a'

        def has_old_key(item):
            global idx
            if item['doi'] not in old_keys:
                return False
            m = re.match(r'[\w-]+[A-Z]+\d\d([a-z])', old_keys[item['doi']])
            if m:
                old_idx = m.group(1)
                item['ID'] = old_keys[item['doi']]
                if old_idx >= idx:
                    idx = chr(ord(old_idx)+1)
                return True
            else:
                return False
        group = [item for item in group if not has_old_key(item)]
        for item in group:
            item['ID'] += idx
            idx = chr(ord(idx)+1)

bibtex.dump(bib, sys.stdout)
