import time
from scraper_tracker import scrape


def get_peer_info(magnet):
    magnet = magnet[20:]
    bthash = magnet.split('&')[0]
    tracker_list = [
        'udp://tracker.zer0day.to:1337/announce'
        'udp://tracker.coppersurfer.tk:6969/announce',
        'udp://tracker.pirateparty.gr:6969/announce',
        'udp://tracker.coppersurfer.tk:6969/announce',
        'udp://opentor.org:2710',
        'udp://tracker.leechers-paradise.org:6969/announce',
        'udp://tracker.zer0day.to:1337/announce'
    ]

    tr = magnet[magnet.find('&tr=')+len('&tr='):].split('&tr=')
    local_tr = '&tr=http://retracker.local/announce'

    tracker_list = list(set(tracker_list))

    t0 = time.time()
    q = []
    for tr in sorted(tracker_list):
        try:
            info = scrape(tr, [bthash])
            print(info)
            for value in info.values():
                q.append(value)

        except Exception as e:
            pass
        #print('='*80)

    max_peer_trackers = sorted(q, key=lambda x: x['seeds'] + x['peers'] + x['complete'], reverse=True)[:30]
    for i in max_peer_trackers:
        print(i)
    print(time.time()-t0)
    m = max_peer_trackers

    return_tr = '&tr='+'&tr='.join([i['tracker'] for i in m]) + local_tr

    if len(max_peer_trackers) == 0:
        print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
        return False
    return (
        max(m, key=lambda x: x['peers'])['peers'],
        max(m, key=lambda x: x['seeds'])['seeds'],
        max(m, key=lambda x: x['complete'])['complete'],
        return_tr,
        bthash
    )

if __name__ == '__main__':
    magnet = 'magnet:?xt=urn:btih:9e4f80a1177dd6568e2c4cfb4f1413a4ca1eb5d9&dn=rutor.info_%D0%A0%D0%B0%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%B0+%2F+The+Accountant+%282016%29+HDRip+%D0%BE%D1%82+MegaPeer+%7C+Line&tr=udp://opentor.org:2710&tr=udp://opentor.org:2710&tr=http://retracker.local/announce'
    peers, seeds, complete, tr, bthash = get_peer_info(magnet)
    print('Seeds: {}\tPeers: {}\tDownloaded: {}'.format(seeds, peers, complete))
    print('magnet:?xt=urn:btih:{}{}'.format(bthash, tr))