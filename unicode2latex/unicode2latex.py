#!/usr/bin/env python3
import sqlite3 as sql
import bibtexparser as bibtex
import sys
import os
import re


db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'unicode2latex.db')


def l2u(text):
    conn = sql.connect(db_path)
    cur = conn.cursor()

    def replace(mobj):
        latex = mobj.group(1)
        unic = cur.execute('select unicode from transl where latex = ?', (latex,)).fetchone()[0]
        return unic

    text = re.sub(r'{(\\[^}]*}?)}', replace, text)
    conn.close()
    return text


def u2l(text):
    conn = sql.connect(db_path)
    cur = conn.cursor()

    def replace(mobj):
        unic = mobj.group(0)
        latex = cur.execute('select latex from transl where unicode = ?', (unic,)).fetchone()
        if not latex:
            return ''
        latex = '{' + latex[0] + '}'
        return latex

    text = re.sub(r'[^\x00-\x7f]', replace, text)
    conn.close()
    return text


def proc_bibtex(text, reverse=False):
    targets = ['author', 'title', 'journal']
    converter = l2u if reverse else u2l
    bib = bibtex.loads(text)
    for item in bib.entries:
        for target in targets:
            item[target] = converter(item[target])
    return bibtex.dumps(bib)


if __name__ == '__main__':
    from argparse import ArgumentParser
    prs = ArgumentParser()
    prs.add_argument('-r', '--reverse',
                     action='store_true',
                     help='convert latex to unicode')
    prs.add_argument('-b', '--bibtex',
                     action='store_true',
                     help='process a bibtex database')
    args = prs.parse_args()
    text = sys.stdin.read()
    if args.bibtex:
        print(proc_bibtex(text, reverse=args.reverse))
    else:
        converter = l2u if args.reverse else u2l
        print(converter(text))
