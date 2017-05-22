#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import bibtexparser as bibtex
import sys
import re
from sciabbr import abbreviate


ignored = ['of', 'the', 'and', 'on', 'für', 'in', '-', '–']
corrections = {
    'Nat': 'Nature',
    'Comms': 'Communications',
    'chemical': 'Chemical',
    'physics': 'Physics'
}
special = {
    'United States of America': 'U. S. A.',
    'A European Journal': 'European Journal'
}


def shorten(word):
    word, suff = re.findall(r'([^:]+)(.*)', word)[0]
    return abbreviate(word) + suff


def process(title):
    for full, abbr in special.items():
        title = title.replace(full, abbr)
    words = [corrections.get(w, w) for w in title.split() if w.lower() not in ignored]
    if len(words) > 1:
        words = [word if word.endswith('.') else shorten(word) for word in words]
    return ' '.join(words)


bib = bibtex.load(sys.stdin)
for item in bib.entries:
    if 'journal' in item:
        item['journal'] = process(item['journal'])
bibtex.dump(bib, sys.stdout)
