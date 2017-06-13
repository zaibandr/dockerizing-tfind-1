from find_torrent.magnet.scraper_tracker import scrape

import time
import psycopg2

conn = psycopg2.connect(
    database='tfind_db',
    user='tfind',
    password='xok43tra',
    host='192.168.1.241',
    port='5432'
)

cur = conn.cursor()

tracker_list = [
        'udp://tracker.zer0day.to:1337/announce'
        'udp://tracker.coppersurfer.tk:6969/announce',
        'udp://tracker.pirateparty.gr:6969/announce',
        'udp://tracker.zer0day.to:1337/announce'
    ]


def get_max(m):
    return (
        max(m, key=lambda x: x['peers'])['peers'],
        max(m, key=lambda x: x['seeds'])['seeds'],
        max(m, key=lambda x: x['complete'])['complete']
    )


def get_bthash():
    t0 = time.time()
    cur.execute("SELECT id, magnet FROM find_torrent_torrent WHERE complete IS NULL LIMIT 74")
    fetch = cur.fetchmany(74)
    print(time.time()-t0)
    print(fetch)
    hashs = []

    hash_d = {}
    for f in fetch:
        id, magnet = f
        magnet = magnet[20:]
        bthash = magnet.split('&')[0]
        hash_d[bthash] = id
        hashs.append(bthash)

    print(hashs)
    # print(time.time()-t0)
    d = {}
    for tr in tracker_list:
        try:
            s = scrape(tr, hashs)
        except Exception as e:
            print(e)
            continue
        for key, value in s.items():
            try:
                d[key].append(value)
            except KeyError:
                d[key] = []
            # print(key, value)

    upds = []
    for t_hash, value in d.items():
        peers, seeds, complete = get_max(value)
        print(t_hash, (peers, seeds, complete), value)

        upds.append((peers, seeds, complete, t_hash, hash_d[t_hash]))

    t1 = time.time()
    cur.executemany("UPDATE find_torrent_torrent SET peers=(%s), seeds=(%s), complete=(%s), t_hash=(%s) WHERE id = (%s)",
                    upds
                    )
    conn.commit()
    print('update peer info: ', time.time()-t1)


if __name__ == '__main__':
    while True:
        t0 = time.time()
        try:
            get_bthash()
        except Exception as e:
            print(e)
        print('='*80)
        print(time.time()-t0)
        print('='*80)
