#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import bibtexparser as bibtex
import sys


allowed_keys = [
    'doi', 'url', 'year', 'volume', 'number', 'pages',
    'author', 'title', 'journal', 'id', 'type', 'ENTRYTYPE', 'ID',
    'publisher'
]
if '--file' in ''.join(sys.argv):
    allowed_keys.append('file')

bib = bibtex.load(sys.stdin)
for item in bib.entries:
    if 'journaltitle' in item and 'journal' not in item:
        item['journal'] = item['journaltitle']
    if 'date' in item and 'year' not in item:
        item['year'] = item['date'].split('-')[0]
    if 'doi' in item:
        item['url'] = 'http://dx.doi.org/{}'.format(item['doi'])
    for k in list(item):
        if k not in allowed_keys:
            del item[k]
bibtex.dump(bib, sys.stdout)
