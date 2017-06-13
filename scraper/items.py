from scrapy.item import Item, Field


class tor_item(Item):
    # define the fields for your item here like:
    provider_url = Field()
    html = Field()

    pass