import requests as r
import time

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
    'X-Compress': 1
}


proxy_list = open('proxy_list.txt', 'r').read().split('\n')
print(list(set(proxy_list)))
url = 'http://rutracker.org/forum/index.php'

for p in proxy_list:
    proxies = {'http': p}
    t0 = time.time()
    try:
        resp = r.get(url, headers=headers, proxies=proxies)
        if resp.status_code == 200 and time.time()-t0 < 2:
            print(resp.text)
            print(p)
    except Exception:
        pass