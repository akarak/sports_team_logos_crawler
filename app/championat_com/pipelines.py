from pathlib import PurePath
from urllib.parse import urlparse

from itemadapter.adapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline


class ChampionatComPipeline:
    def process_item(self, item, spider):
        return item


class TeamLogoFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        adapter: ItemAdapter = ItemAdapter(item)
        item_name: str = adapter["name"]
        item_country: str = adapter["country"]

        ext: str = PurePath(urlparse(request.url).path).suffix

        return f"{item_name}, {item_country}{ext}"
