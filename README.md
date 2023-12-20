cd app

scrapy genspider teams https://www.championat.com/football/_russiacup/tournament/5475/teams/

scrapy list
scrapy crawl teams -a "start_url=https://www.championat.com/football/_russiacup/tournament/5475/teams/"

Изменено значение USER_AGENT в settings.py для исправления ошибки 403.

USER_AGENT = "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"