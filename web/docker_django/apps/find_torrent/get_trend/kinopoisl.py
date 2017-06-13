import requests as r
from bs4 import BeautifulSoup
import datetime
import time

from find_torrent.get_trend.insert_data import insert_trend

months = list(map(str, range(1, 13)))
days = list(map(str, range(1, 32)))
print(months)

year = '2016'


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
    'Connection': 'keep-alive',
    'Host': 'www.kinopoisk.ru',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
    'X-Compress': 1
}


def pars_trend(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.title.text)

    stat = soup.find("div", class_='stat')

    for div in stat.find_all('div'):
        # print(div)
        '''
        <div class="el" id="obj468522">
        <b><a href="/film/468522/popular/." style="color:#f60;font-size:12px">1</a></b>
        <a href="/film/468522/" style="font:100 12px arial,sans-serif">Отряд самоубийц (2016)</a>
        <i>Suicide Squad</i>
        </div>
        '''
        try:
            # second link text in div
            name = div.find_all('a')[1].text

            insert_trend({'title': str(name)})
            # trend.write('{}\n'.format(str(name)))
        except IndexError as e:
            pass
        # print('='*30)


def main(day_count=0):
    count = {}
    for month in reversed(months):
        for day in reversed(days):
            for page in range(1, 21):
                try:
                    date_s = '-'.join([year, month, day])
                    # print(date_s)
                    date = datetime.datetime.strptime(date_s, '%Y-%m-%d').date()
                    if datetime.date.today() > date:
                        count[date] = True

                        url = 'https://www.kinopoisk.ru/popular/day/{}/page/{}/'.format(date, page)
                        print(url)
                        resp = r.get(url, headers=headers)

                        # print(resp.text)
                        pars_trend(resp.text)

                        # time.sleep(0.5)
                except ValueError as e:
                    print(e)

            if 0 < day_count <= len(count.keys()):
                return True

if __name__ == '__main__':
    print(main(30))