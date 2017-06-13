from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scraper.parsers import thepiratebay_to_torrent


class The_Pirate_Bay(CrawlSpider):
    name = "thepiratebay.org"
    allowed_domains = ["thepiratebay.org"]
    start_urls = [
        "https://thepiratebay.org/browse",
        "https://thepiratebay.org/tv/",
        "https://thepiratebay.org/top",
        "https://thepiratebay.org/recent",
        "https://thepiratebay.org/music"
    ]

    #http://top-tor.org/tag/8/3rd%20Person
    #http://rutor.info/torrent/534342/otrjad-samoubijc_suicide-squad-2016-web-dl-1080p-ot-exkinoray-theatrical-cut-itunes
    #http://rutor.info/tag/1/%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F
    rules = (
        Rule(LinkExtractor(allow=(r'.*/browse/.*',)), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=(r'.*/.*/.*/.*/',)), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=(r'.*/.*/.*/',)), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=(r'.*/.*/',)), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        thepiratebay_to_torrent(response.body)