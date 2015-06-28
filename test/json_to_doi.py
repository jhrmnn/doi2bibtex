#!/usr/bin/env python3
import json
import sys


raw = json.load(sys.stdin)
dois = [item.get('DOI', item['title'])
        for item in raw
        if item['type'] == 'article-journal']
for doi in dois:
    print(doi)
