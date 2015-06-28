#!/usr/bin/env python3
from urllib.request import Request, urlopen
from queue import Queue
from threading import Thread
import sys


def worker(queue, results):
    root = 'http://doi.org/'
    while not queue.empty():
        doi = queue.get()
        req = Request(root + doi,
                      headers={'Accept': 'application/x-bibtex'})
        with urlopen(req) as rsp:
            response = rsp.read().decode('utf-8')
        results.append(response)
        queue.task_done()


dois = Queue()
db = []
for l in sys.stdin:
    dois.put(l.strip())
for i in range(50):
    thr = Thread(target=worker, args=(dois, db))
    thr.start()
dois.join()
print('\n'.join(db))
