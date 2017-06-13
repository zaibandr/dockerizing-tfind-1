from sort_info import get_peer_info
from Magnet_To_Torrent2 import magnet2torrent
import PTN
import psycopg2
import json

conn = psycopg2.connect(
    database='tfind_db',
    user='tfind',
    password='xok43tra',
    host='192.168.1.241',
    port='5432'
)

cur = conn.cursor()


def update_one(f, m2t=False):
    id, title, magnet = f
    print('='*80)
    print(id)

    peer_info = get_peer_info(magnet)
    if not peer_info:
        print('get_per_info error, continue...')
        return False
    peers, seeds, complete, tr, bthash = peer_info
    print('Seeds: {}\tPeers: {}\tDownloaded: {}'.format(seeds, peers, complete))

    new_magnet = 'magnet:?xt=urn:btih:{}{}'.format(bthash, tr)
    print(new_magnet)

    if not m2t:
        cur.execute(" UPDATE find_torrent_torrent SET peers=(%s), seeds=(%s), complete=(%s), magnet=(%s) WHERE id = (%s)",
                        (peers, seeds, complete, new_magnet, id)
                    )
        conn.commit()
    else:
        try:
            t_name, t_files = magnet2torrent(new_magnet)
            print(t_name)

            new_magnet = 'magnet:?xt=urn:btih:{}&dn={}{}'.format(bthash, t_name, tr)

            t_files = [i for i in t_files]
            print(t_files)

            name_pars = PTN.parse(t_name)
            print(name_pars)

            cur.execute("UPDATE find_torrent_torrent SET peers=(%s), seeds=(%s), complete=(%s), magnet=(%s), file_list=(%s), name_pars=(%s) WHERE id = (%s)",
                            (peers, seeds, complete, new_magnet, json.dumps(t_files), json.dumps(name_pars),  id)
                            )
            conn.commit()
        except Exception as e:
            print(e)
            cur.execute("UPDATE find_torrent_torrent SET peers=(%s), seeds=(%s), complete=(%s), magnet=(%s) WHERE id = (%s)",
                            (peers, seeds, complete, new_magnet, id)
                            )
            conn.commit()

    print('='*80)


if __name__ == '__main__':
    cur.execute("SELECT id, title, magnet FROM find_torrent_torrent WHERE complete IS NOT NULL AND file_list IS NULL ORDER BY complete DESC LIMIT 200")
    fetch = cur.fetchmany(200)
    for f in fetch:
        update_one(f=f, m2t=True)
