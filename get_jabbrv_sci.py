#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import sqlite3 as sql
from io import StringIO

url = 'http://journal-abbreviations.library.ubc.ca/dump.php'
with urlopen(url) as rsp:
    raw = rsp.read().decode('utf-8')
html = json.load(StringIO(raw[1:-2]))['html']
tree = BeautifulSoup(html)
db = []
for row in tree.find('tbody').children:
    if len(row.contents) == 2 and row.contents[0].text:
        abbr, full = row.contents[0].text, row.contents[1].text
        db.append((abbr, full))
conn = sql.connect('jabbrev.sqlite')
cur = conn.cursor()
cur.execute('drop table if exists abbrevs')
cur.execute('create table abbrevs (abbrev text, full text)')
cur.executemany('insert into abbrevs values (?,?)', db)
conn.commit()
conn.close()
