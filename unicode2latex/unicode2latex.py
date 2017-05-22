#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Converts Unicode letters to Latex escape codes.

Usage:
    unicode2latex.py [-r] [-b]

Options:
    -r, --reverse             Convert Latex to Unicode.
    -b, --bibtex              Assume the input stream is Bibtex.
"""
from docopt import docopt
import sqlite3 as sql
import bibtexparser as bibtex
from bibtexparser.bparser import BibTexParser
import sys
import os
import re
import unicodedata


db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'unicode2latex.db')


def l2u(text):
    conn = sql.connect(db_path)
    cur = conn.cursor()

    def replace(mobj):
        latex = mobj.group(1)
        unic = cur.execute('select unicode from transl where latex = ?', (latex,)).fetchone()
        if not unic:
            raise RuntimeError('Unknown latex sequence: {}'.format(latex))
        return unic[0]

    text = re.sub(r'{(\\[^}]*}?)}', replace, text)
    text = unicodedata.normalize('NFC', text)
    conn.close()
    return text


def u2l(text):
    conn = sql.connect(db_path)
    cur = conn.cursor()

    def replace(mobj):
        unic = mobj.group(0)
        latex = cur.execute('select latex, mode from transl where unicode = ?', (unic,)).fetchone()
        if not latex:
            raise RuntimeError('Unknown Unicode character: {}'.format(unic))
        latex, mode = latex
        sep = '$' if mode == 'math' else ''
        latex = '{' + sep + latex + sep + '}'
        return latex

    text = re.sub(r'[^\x00-\x7f]', replace, text)
    conn.close()
    return text


def proc_bibtex(text, reverse=False):
    targets = ['author', 'title', 'journal']
    converter = l2u if reverse else u2l
    parser = BibTexParser()
    parser.homogenise_fields = False
    bib = bibtex.loads(text, parser)
    for item in bib.entries:
        for target in targets:
            if target not in item:
                continue
            if '\$' in item[target]:
                sys.stderr.write('error: quoted latex math expression in {}:{}, abort\n'
                                 .format(item['id'], target))
                sys.exit(1)
            elif '$' in item[target]:
                sys.stderr.write('warning: latex math expression in {}:{}, skipping\n'
                                 .format(item['id'], target))
                continue
            item[target] = converter(item[target])
    return bibtex.dumps(bib)


if __name__ == '__main__':
    args = docopt(__doc__)
    text = sys.stdin.read()
    if args['--bibtex']:
        print(proc_bibtex(text, reverse=args['--reverse']))
    else:
        converter = l2u if args['--reverse'] else u2l
        print(converter(text))
