# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import xml.etree.ElementTree as ET
import sqlite3 as sql
import sys
import unicodedata

db_path = sys.argv[1]


def process():
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    db = []
    for char in root.findall('character'):
        mode = char.attrib.get('mode')
        latex = char.find('latex')
        if latex is not None:
            try:
                unic = unicodedata.lookup(char.find('description').text.strip())
            except KeyError:
                continue
            db.append((unic, latex.text.strip(), mode))
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute('drop table if exists transl')
    cur.execute('create table transl (unicode text, latex text, mode text)')
    conn.commit()
    cur.executemany('insert into transl values (?,?,?)', db)
    conn.commit()
    conn.close()


process()
