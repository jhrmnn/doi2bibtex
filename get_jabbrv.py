#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3 as sql
import string
from multiprocessing import Pool

url = 'http://images.webofknowledge.com/WOK46/help/WOS/{}_abrvjt.html'
parts = ['0-9'] + list(string.ascii_uppercase)
conn = sql.connect('jabbrev.sqlite', timeout=30)
cur = conn.cursor()
cur.execute('drop table if exists abbrevs')
cur.execute('create table abbrevs (abbrev text, full text)')
conn.commit()


def worker(part):
    with urlopen(url.format(part)) as rsp:
        html = rsp.read().decode('utf-8')
    html = html.replace('<B>', '').replace('</B>', '')
    lst = BeautifulSoup(html).find('dl')
    items = lst.find_all(['dt', 'dd'])
    db = []
    for full, abbrev in zip(items[::2], items[1::2]):
        db.append((abbrev.text.strip(), full.text.strip()))
    cur.executemany('insert into abbrevs values (?,?)', db)
    conn.commit()

pool = Pool()
pool.map(worker, parts)
conn.close()
