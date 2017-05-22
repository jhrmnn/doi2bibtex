#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json
import sys


raw = json.load(sys.stdin)
dois = [item.get('DOI', item['title'])
        for item in raw
        if item['type'] == 'article-journal']
for doi in dois:
    print(doi)
