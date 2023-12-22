# Утилита для скачивания изображений с логотипами спортивных команд

## Управление

Управление утилитой выполняется через параметры командной строки. Задание на скачивание передаётся в виде имени текстового файла в формате `json`, содержащего два поля: адрес страницы, с которой выполняется скачивание, и префикс, добавляемый в названия скачиваемых файлов.

```json
{
    "url": "https://.../_russiacup/tournament/5475/teams/",
    "prefix": "Спорт. Логотипы команд. Футбол. Чемпионат России 2023-2024. "
}
```

Файлы с заданиями должны находиться в папке `tasks`.

Скачанные файлы переименовываются на основе формата `<префикс> <название команды>, <город или страна>`, конвертируются в формат `tga` с компрессией и помещаются в папку `output`.

Пути к папкам `tasks` и `output` передаются через параметры `--tasks_dir` и `--output_dir`.

Для упрощения разворачивания утилита упакована в образ [Docker](https://www.docker.com/products/docker-desktop/).

## Запуск в Docker

### Сборка

Для сборки `image` необходимо в папке с проектом (файлом `Dockerfile`) выполнить команду `build`. Здесь и далее все команда приведены для [PowerShell](https://github.com/PowerShell/PowerShell/).

```powershell
docker build --tag sports_team_logos_crawler .
```

### Запуск

В образе используются две папки с фиксированным именем и расположением:
- `/output` для сохранения скачанных изображений;
- `/tasks` для хранения файлов с заданиями.

Для доступа к содержимому папок с хоста необходимо с помощью `volume` связать эти папки с папками на хосте.

```powershell
docker run --rm `
    --volume c:\\temp\\output:/output --volume c:\\temp\\tasks:/tasks:ro `
    --env http_proxy=$env:http_proxy --env https_proxy=$env:https_proxy `
    sports_team_logos_crawler:latest football_russian_cup.json
```

### Отладка

```powershell
docker run --rm -it sports_team_logos_crawler:latest bash
```
