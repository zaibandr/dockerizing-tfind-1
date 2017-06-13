from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scraper.parsers import rutracker_to_torrent


class Fast_Torrent(CrawlSpider):
    http_user = 'panagoa'
    http_pass = '050595'

    name = "rutracker.org"
    allowed_domains = ["rutracker.org"]

    start_urls = ["http://rutracker.org/forum/index.php"]

    #http://top-tor.org/tag/8/3rd%20Person
    #http://rutor.info/torrent/534342/otrjad-samoubijc_suicide-squad-2016-web-dl-1080p-ot-exkinoray-theatrical-cut-itunes
    #http://rutor.info/tag/1/%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F
    rules = (
        Rule(LinkExtractor(allow=(r'.*forum/viewtopic.php\?t=\d*',)), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=(r'.*forum/viewforum.php\?f=\d*',)), follow=True),
        Rule(LinkExtractor(allow=(r'.*forum/index.php\?c=\d*',)), follow=True),

    )

    def parse_item(self, response):
        # print(response.body)
        rutracker_to_torrent(response.body, response.url)