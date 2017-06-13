from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scraper.parsers import rutor_to_torrent


class Fast_Torrent(CrawlSpider):
    name = "rutor.info"
    allowed_domains = ["rutor.info"]


    #cur.execute("SELECT title, count_check FROM find_torrent_trend WHERE count_check is NULL AND priority >= 2 ORDER BY priority DESC")
    #fetchs = cur.fetchmany(1000)
    #
    #start_urls = ['http://rutor.info/search/0/0/100/0/{}'.format(f[0]) for f in fetchs]
    #print(start_urls)


    start_urls = ['http://rutor.info',
                  'http://rutor.info/top',
                  'http://rutor.info/browse/',
                  'http://rutor.info/categories']

    #http://top-tor.org/tag/8/3rd%20Person
    #http://rutor.info/torrent/534342/otrjad-samoubijc_suicide-squad-2016-web-dl-1080p-ot-exkinoray-theatrical-cut-itunes
    #http://rutor.info/tag/1/%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F

    rules = (
        Rule(LinkExtractor(allow=(r'http://rutor.info/*',)), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        rutor_to_torrent(response.body)