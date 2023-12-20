from scrapy import Item, Field


class TeamItem(Item):
    files = Field()
    file_urls = Field()

    logo_url = Field()
    name = Field()
    country = Field()
