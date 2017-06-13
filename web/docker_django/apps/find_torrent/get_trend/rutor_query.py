# -*- coding: utf-8 -*-
import requests as r
import datetime
import random
import time

from find_torrent.scraper.parsers import rutor_to_torrent

import logging

import psycopg2

conn = psycopg2.connect(
    database='tfind_db',
    user='tfind',
    password='xok43tra',
    host='192.168.1.241',
    port='5432'
)

cur = conn.cursor()


# Logging settint
logging.basicConfig(format='%(asctime)s %(message)s', filename='rutor_query_{}.log'.format(datetime.date.today()))
logger = logging.getLogger(__name__)

# request headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'rutor.info',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
    'X-Compress': 1
}

proxy_list = open('proxy_list.txt', 'r').read().split('\n')
print(proxy_list)


def get_search_result(q):
    logger.info('q: {}'.format(q))
    print(q)
    if len(q) >= 3:
        q = q.replace('мини-сериал, ', '')
        q = q.replace('сериал, ', '')
    else:
        return False
    url = 'http://rutor.info/search/0/0/100/0/{}'.format(q)

    logger.info('url{}'.format(url))

    rnd_proxy = random.choice(proxy_list)
    proxies = {'http': rnd_proxy}
    try:
        resp = r.get(url, headers=headers, proxies=proxies)
        # print(resp.headers)
        # print(work_proxy)
        # work_proxy.append(proxies)
    except Exception as e:
        print(e)
        return False

    return resp.text


# cur.execute("SELECT title FROM find_torrent_trend WHERE last_check=(%s)", ('Null',))
cur.execute("SELECT title, count_check FROM find_torrent_trend WHERE count_check is NULL AND priority >= 2 ORDER BY priority DESC")
fetchs = cur.fetchmany(2000)
print(len(fetchs))
time.sleep(2)


def loop(sleep_sec=0):
    # last 24 hours torrents
    rutor_to_torrent(r.get('http://rutor.info/', headers=headers).text)

    for i, fetch in enumerate(fetchs):
        print('\t\t', i)
        q, count_check = fetch
        print(q, count_check)
        if count_check is None:
            count_check = 0

        html = get_search_result(q)
        if html:
            rutor_to_torrent(html)
            cur.execute("UPDATE find_torrent_trend SET last_check=(%s), count_check=(%s) WHERE title = (%s)",
                        (datetime.date.today(), count_check+1, q)
                        )
            conn.commit()

            time.sleep(sleep_sec)

loop(sleep_sec=0)
