import argparse
from pathlib import Path
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from championat_com.spiders import TeamsSpider
from core.image_transformations import convert_to_tga_without_transparent_margins
from core.task import Task, load_task


def get_scrapy_settings(args: argparse.Namespace):
    settings: Settings = get_project_settings()
    settings["USER_AGENT"] = (
        "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    )
    settings["ROBOTSTXT_OBEY"] = False
    settings["ITEM_PIPELINES"] = {
        "championat_com.pipelines.FilesPipeline_WithoutFullDir": 400,
#        "scrapy.pipelines.files.FilesPipeline": 400,
    }
    settings["FILES_STORE"] = args.output_dir

    return settings


def main(args: argparse.Namespace):
    # TODO: Обрабатывать FileNotFoundError
    crawler_task: Task = load_task(str(Path(args.tasks_dir, args.task)))

    scraped_items = []

    def item_scraped_handler(signal, sender, item, response, spider):
        scraped_items.append(item)

    dispatcher.connect(item_scraped_handler, signal=signals.item_scraped)

    scrapy_settings: Settings = get_scrapy_settings(args)
    process = CrawlerProcess(scrapy_settings)
    process.crawl(
        TeamsSpider,
        start_url=crawler_task.url,
    )
    # TODO: Перейти на асинхронное создание файла после получения сигнала.
    process.start()

    filepath_dir: str = scrapy_settings["FILES_STORE"]
    for item in scraped_items:
        for file in item["files"]:
            filepath_src: Path = Path(filepath_dir, file["path"])
            filename_dest: Path = convert_to_tga_without_transparent_margins(filepath_src)
            Path(filepath_src).unlink()
            Path(filepath_dir, filename_dest).rename(
                Path(
                    filepath_dir,
                    f"{crawler_task.prefix}{item['name']}, {item['country']}{filename_dest.suffix}",
                )
            )

    return scraped_items


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Утилита для скачивания логотипов спортивных команд"
    )
    parser.add_argument(
        "--output_dir",
        "-o",
        dest="output_dir",
        type=str,
        required=True,
        help="Путь к папке со скачанными файлами",
    )
    parser.add_argument(
        "--tasks_dir",
        "-t",
        dest="tasks_dir",
        type=str,
        required=True,
        help="Путь к папке с заданиям для скачивания",
    )
    parser.add_argument(
        "task",
        type=str,
        help="Имя файла с заданием",
    )

    try:
        # args = parser.parse_args(
        #     [
        #         r"--output_dir=C:\Temp\output",
        #         r"--tasks_dir=C:\Temp\tasks",
        #         "football_russian_cup.json",
        #     ]
        # )
        args = parser.parse_args()
        main(args)
    except SystemExit as e:
        pass
