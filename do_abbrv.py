#!/usr/bin/env python3
import bibtexparser as bibparse
import sqlite3 as sql
import sys

conn = sql.connect('jabbrv.sqlite')
cur = conn.cursor()
bib = bibparse.load(sys.stdin)
for item in bib.entries:
    journal = item['journal']
    if cur.execute('select * from abbrvs where abbrev=?',
                   (journal.replace('.', '').upper(),)).fetchone():
        print('ABBREVIATED')
        continue  # already abbreviated
    abbrev = cur.execute('select abbrev from abbrvs where full=?',
                         (journal.upper(),)).fetchone()
    abbrev = abbrev.capitalize()
    print(journal, abbrev)
