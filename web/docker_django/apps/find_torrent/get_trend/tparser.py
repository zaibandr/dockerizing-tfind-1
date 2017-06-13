import requests
import time
import json

from find_torrent.get_trend.insert_data import insert_trend


def loop(limit=0, sleep_sec=5):
    i = 0
    while not limit or i < limit:
        resp = requests.get('http://tparser.org/js3/get.php')
        s = resp.text[len('multi({"key":'):-2]
        for d in json.loads(s):
            trend = {'title': d['k']}
            print(trend)
            insert_trend(trend)
        i += 1
        print('='*80)
        time.sleep(sleep_sec)

loop(0, sleep_sec=60)
