from pathlib import Path
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from championat_com.spiders import TeamsSpider
from core.image_transformations import convert_to_tga_without_transparent_margins


def get_settings():
    settings: Settings = get_project_settings()
    settings["USER_AGENT"] = (
        "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    )
    settings["ROBOTSTXT_OBEY"] = False
    settings["ITEM_PIPELINES"] = {
        "championat_com.pipelines.TeamLogoFilesPipeline": 400,
    }
    settings["FILES_STORE"] = "./files/"

    return settings


def main():
    files = []

    def crawler_results(signal, sender, item, response, spider):
        target_path: str = spider.settings["FILES_STORE"]
        files.extend(str(Path(target_path, d["path"])) for d in item["files"])

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process = CrawlerProcess(get_settings())
    process.crawl(
        TeamsSpider,
        start_url="https://www.championat.com/football/_russiacup/tournament/5475/teams/",
    )
    process.start()

    for filepath in files:
        try:
            convert_to_tga_without_transparent_margins(filepath)
            Path(filepath).unlink()
        except:
            pass

    return files


if __name__ == "__main__":
    print(main())


# TODO: Адрес страницы и префикс названия файлов передавать в TeamsSpider через параметры.
# TODO: очищать папку files перед запуском.
# TODO: проверить с прокси. подготовить докерфайл, в который мепится путь на папку files и передаётся линк на сайт.
# TODO: залить в чистый проект на github.
# TODO: добавить асинхронное создание файла после получения сигнала.


# Кубок России по футболу
# https://www.championat.com/football/_russiacup/tournament/5475/teams/

# РПЛ. Футбол
# https://www.championat.com/football/_russiapl/tournament/5441/teams/
