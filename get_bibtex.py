#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from urllib.request import Request, urlopen
from queue import Queue
from threading import Thread
import sys


def worker(queue, results):
    root = 'http://data.crossref.org/'
    while not queue.empty():
        doi = queue.get()
        req = Request(root + doi, headers={'Accept': 'application/x-bibtex'})
        with urlopen(req) as rsp:
            response = rsp.read().decode()
        results.append(response)
        queue.task_done()


dois = Queue()
db = []
for l in sys.stdin:
    dois.put(l.strip())
for i in range(20):
    thr = Thread(target=worker, args=(dois, db))
    thr.start()
dois.join()
print('\n'.join(db))
