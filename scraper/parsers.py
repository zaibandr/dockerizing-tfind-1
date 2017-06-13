from bs4 import BeautifulSoup
import re
import requests

from .db_insert import insert_torrent_db


def extratorrent_to_torrent(html):
    # soup = BeautifulSoup(open('q.html', 'r'), 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')

    # Dumping to files
    # dump_f = open('dump_query_rutor_{}.txt'.format(datetime.date.today()), 'a+')

    provider = 'http://extratorrent.cc'
    provider_name = 'Extratorrent.cc'

    for tr in soup.find_all('tr', class_=re.compile('^tlr$|^tlz$')):
        print('tr', tr)
        a_list = tr.find_all('a')
        # print(a_list)
        d = {}
        try:
            d['title'] = a_list[2].text
            d['magnet'] = a_list[1].get('href')
            d['provider'] = provider_name
            d['provider_url'] = provider + a_list[2].get('href')
            # print(d)
            # dump_f.write(json.dumps(d)+'\n')

            # Dumping to files
            # dump_f.write(str(d)+'\n')

            # Insert to database (Postgresql)
            insert_torrent_db(d)

        except Exception as e:
            print(e)


def rutor_to_torrent(html):
    # soup = BeautifulSoup(open('q.html', 'r'), 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')

    # Dumping to files
    # dump_f = open('dump_query_rutor_{}.txt'.format(datetime.date.today()), 'a+')

    provider = 'http://rutor.info'
    provider_name = 'Rutor.info'

    for tr in soup.find_all('tr', class_=re.compile('^gai$|^tum$')):
        a_list = tr.find_all('a')
        # print(a_list)
        d = {}
        try:
            d['title'] = a_list[2].text
            d['magnet'] = a_list[1].get('href')
            d['provider'] = provider_name
            d['provider_url'] = provider + a_list[2].get('href')
            # print(d)
            # dump_f.write(json.dumps(d)+'\n')

            # Dumping to files
            # dump_f.write(str(d)+'\n')

            # Insert to database (Postgresql)
            insert_torrent_db(d)

        except Exception as e:
            print(e)


def rutracker_to_torrent(html, url=0):
    # soup = BeautifulSoup(open('q.html', 'r'), 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')


    # Dumping to files
    # dump_f = open('dump_query_rutor_{}.txt'.format(datetime.date.today()), 'a+')

    provider = 'http://rutracker.org/forum/'
    provider_name = 'RuTracker.org'

    d = {}
    try:
        d['title'] = str(soup.find('h1').text).replace('\n', '')
        d['magnet'] = soup.find('a', class_=re.compile('.*magnet-link.*')).get('href')
        d['provider'] = provider_name
        d['provider_url'] = url


        # print(d)
        # dump_f.write(json.dumps(d)+'\n')
        # Dumping to files
        # dump_f.write(str(d)+'\n')
        # Insert to database (Postgresql)
        insert_torrent_db(d)
    except Exception as e:
        print(e)


def thepiratebay_to_torrent(html):
    # soup = BeautifulSoup(open('q.html', 'r'), 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')

    # Dumping to files
    # dump_f = open('dump_query_rutor_{}.txt'.format(datetime.date.today()), 'a+')

    provider = 'https://thepiratebay.org'
    provider_name = 'ThePirateBay.org'

    for tr in soup.find_all('tr'):
        a_list = tr.find_all('a')
        # print(a_list)
        d = {}
        try:
            d['title'] = a_list[2].text
            d['magnet'] = a_list[3].get('href')
            d['provider'] = provider_name
            d['provider_url'] = provider + a_list[2].get('href')

            if not re.match('^magnet:', d['magnet']):
                continue
            # print(d)
            # dump_f.write(json.dumps(d)+'\n')

            # Dumping to files
            # dump_f.write(str(d)+'\n')

            # Insert to database (Postgresql)
            insert_torrent_db(d)
            # print(d)

        except Exception as e:
            print(e)

    #link_filter = re.compile('^/')
    #return list(filter(link_filter.match, [li.get('href') for li in soup.find_all('a')]))


if __name__ == '__main__':
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.torrentino.me',
        'Referer': 'http://www.torrentino.me/movie/993186-fishtales',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
        'X-Compress': 1
    }

    cookies = dict(PHPSESSID='61hv9ha0meiebdq88m9clan3c1', _ym_uid='1481326108509977351', _ym_isad='2',  _gat='1', _ga='GA1.2.934493101.1481326111', _ym_visorc_39142865='w')
    print(requests.get('http://www.torrentino.me/search?search=radiohead', cookies=cookies).text)