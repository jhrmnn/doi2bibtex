#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3 as sql
from multiprocessing import Pool, Value
from queue import Queue, Empty
from threading import Thread


def chunker(lst, n):
    """Divides lst to n chunks so that their sizes differ at most by one."""
    k = len(lst)//n
    nleft = len(lst)-n*k
    sizes = nleft*[k+1] + (n-nleft)*[k]
    j = 0
    for i in range(n):
        yield lst[j:j+sizes[i]]
        j += sizes[i]


url_tmpl = 'http://www.issn.org/services/online-services/access-to-the-ltwa/?numpage={}'
db_path = 'jabbrv.db'


def db_init():
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute('drop table if exists abbrvs')
    cur.execute('create table abbrvs (full text, abbr text, lang text)')
    conn.commit()
    conn.close()


def get_page_count():
    with urlopen(url_tmpl.format(1)) as rsp:
        html = rsp.read().decode()
    n = int(BeautifulSoup(html).find('span', class_='extend').a.text)
    print('{} pages to be downloaded'.format(n))
    return n


db_init()
n_pages = get_page_count()
n_downloaded = Value('i', 0)  # shared counter


def downloader(url_que, html_que):
    while True:
        try:
            url = url_que.get_nowait()
        except Empty:
            return
        try:
            with urlopen(url) as rsp:
                html = rsp.read().decode()
        except:
            print('error: {} not downloaded, will try again'.format(url))
            url_que.put(url)
        else:
            html_que.put((url, html))
            with n_downloaded.get_lock():
                n_downloaded.value += 1
                print('{}/{} downloaded'.format(n_downloaded.value, n_pages))
        finally:
            url_que.task_done()


def scraper(html_que):
    conn = sql.connect(db_path, timeout=30)
    cur = conn.cursor()
    while True:
        try:
            url, html = html_que.get(timeout=1)
        except Empty:
            continue
        tree = BeautifulSoup(html)
        db = []
        for row in tree.find('table', class_='liste-abrev').find_all('tr'):
            items = row.find_all('td')
            if not items:
                continue
            db.append(tuple(it.text for it in items))
        cur.executemany('insert into abbrvs values (?,?,?)', db)
        conn.commit()
        html_que.task_done()


def worker(urls):
    url_que = Queue()
    html_que = Queue()
    for url in urls:
        url_que.put(url)
    for i in range(10):
        Thread(target=downloader, args=(url_que, html_que)).start()
    Thread(target=scraper, args=(html_que,), daemon=True).start()
    url_que.join()
    html_que.join()


urls = [url_tmpl.format(i) for i in list(range(1, n_pages+1))]
pool = Pool()
pool.map(worker, chunker(urls, pool._processes))
