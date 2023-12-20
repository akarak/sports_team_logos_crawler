from urllib.parse import urlparse
from scrapy import Spider
from scrapy.http import Response

from ..items import TeamItem


class TeamsSpider(Spider):
    name = "teams"

    def __init__(self, start_url: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_domains = [urlparse(start_url).hostname]
        self.start_urls = [start_url]

    def parse(self, response: Response):
        teams = response.xpath("//div[@class='teams']/div[@class='teams-item']")
        for team in teams:
            item = TeamItem()
            item["logo_url"] = team.xpath(".//img[@class='teams-item__photo']/@src").get()
            item["name"] = team.xpath(".//div[@class='teams-item__name']/text()").get()
            item["country"] = team.xpath(".//div[@class='teams-item__country']/text()").get()

            item["file_urls"] = [item["logo_url"]]

            yield item
