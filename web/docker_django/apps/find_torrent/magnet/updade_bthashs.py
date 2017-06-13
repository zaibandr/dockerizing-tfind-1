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
        'udp://tracker.coppersurfer.tk:6969/announce',
        'udp://opentor.org:2710',
        'udp://tracker.leechers-paradise.org:6969/announce',
        'udp://tracker.zer0day.to:1337/announce'
    ]


class NotNewTorrent(Exception):
    def __str__(self):
        return "Not found new torrent"


class FewScrapedTracker(Exception):
    def __str__(self):
        return "Few tracker scraped"


def get_max(m):
    if len(m) < 2:
        raise FewScrapedTracker
    return (
        max(m, key=lambda x: x['peers'])['peers'],
        max(m, key=lambda x: x['seeds'])['seeds'],
        max(m, key=lambda x: x['complete'])['complete']
    )


def get_bthash():
    t0 = time.time()
    cur.execute("SELECT id, magnet FROM find_torrent_torrent WHERE complete IS NULL LIMIT 74")
    fetch = cur.fetchmany(74)

    if len(fetch) < 74:
        raise NotNewTorrent

    print(time.time()-t0)
    print(fetch)
    hashs = []

    upds = []
    for f in fetch:
        id, magnet = f
        magnet = magnet[20:]
        bthash = magnet.split('&')[0]
        upds.append((bthash, id))
        hashs.append(bthash)

    t1 = time.time()
    cur.executemany("""UPDATE find_torrent_torrent SET t_hash=(%s) WHERE id = (%s)""",
                    upds
                    )
    conn.commit()

    update_t_hash_time = time.time()-t1
    print('update t_hash: ', update_t_hash_time)

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
        try:
            peers, seeds, complete = get_max(value)
            print(t_hash, (peers, seeds, complete), value)

            upds.append((peers, seeds, complete, t_hash))
        except FewScrapedTracker as e:
            print(e)
            break

    t1 = time.time()
    cur.executemany("UPDATE find_torrent_torrent SET peers=(%s), seeds=(%s), complete=(%s) WHERE t_hash = (%s)",
                    upds
                    )
    conn.commit()
    update_peer_info_time = time.time()-t1
    print('update peer info: ', update_peer_info_time)
    return time.time()-t0, update_t_hash_time, update_peer_info_time


if __name__ == '__main__':
    import logging

    # Logging settint
    logging.basicConfig(format='%(asctime)s %(message)s', filename='update_hash.log')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    times = []
    while True:
        t0 = time.time()
        try:
            times.append(get_bthash())
        except NotNewTorrent as e:
            print(e)
            print('60 sec sleeping..')
            time.sleep(60)
        except Exception as e:
            print(e)

        print('='*80)
        print(time.time()-t0)
        print('='*80)
        if len(times) == 10:
            logger.info(sum([i[0] for i in times])/len(times))
            logger.info(sum([i[1] for i in times])/len(times))
            logger.info(sum([i[2] for i in times])/len(times))
            logger.info('='*80)
            times = []
