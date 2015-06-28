import xml.etree.ElementTree as ET
import sqlite3 as sql
import sys
import unicodedata

db_path = 'unicode2latex.db'


def process():
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    db = []
    for char in root.findall('character'):
        latex = char.find('latex')
        if latex is not None:
            try:
                unic = unicodedata.lookup(char.find('description').text.strip())
            except KeyError:
                continue
            db.append((unic, latex.text.strip()))
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute('drop table if exists transl')
    cur.execute('create table transl (unicode text, latex text)')
    conn.commit()
    cur.executemany('insert into transl values (?,?)', db)
    conn.commit()
    conn.close()


process()
