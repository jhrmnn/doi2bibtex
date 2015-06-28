#!/usr/bin/env python3
import bibtexparser as bibtex
import sqlite3 as sql
import sys
from collections import namedtuple
import re
import os


ignored = ['of', 'the']
corrections = {
    'Nat': 'Nature',
    'Comms': 'Communications'
}

Recd = namedtuple('Recd', ('full', 'abbr', 'lang', 'type'))

db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jabbrv.db')
conn = sql.connect(db_path)
cur = conn.cursor()


def shorten(word):
    word, suff = re.findall(r'([^:]+)(.*)', word)[0]
    is_capital = word[0].isupper()
    recds = [Recd(*abbr) for abbr in
             cur.execute('select * from abbrvs where ? like full', (word,))]
    if recds:
        if len(recds) > 1:
            fulls = [r for r in recds if r.type == 0]
            if len(fulls) == 1:
                # if only one non-affix abbreviation
                recds = fulls
            elif all(r.abbr == recds[0].abbr for r in recds):
                # if all abbreviations equivalent
                pass
            else:
                for recd in recds:
                    print(recd)
                raise Exception('Multiple nonequivalent abbreviations possible')
        abbr = recds[0].abbr
        if abbr != 'n.a.':
            word = abbr
    return (word.capitalize() if is_capital else word) + suff


def process(title):
    words = [corrections.get(w, w) for w in title.split()
             if w.lower() not in ignored]
    if len(words) > 1:
        words = [shorten(word) if not word.endswith('.') else word
                 for word in words]
    return ' '.join(words)


bib = bibtex.load(sys.stdin)
for item in bib.entries:
    item['journal'] = process(item['journal'])
bibtex.dump(bib, sys.stdout)
