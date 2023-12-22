# Запуск в Docker

## Сборка и запуск

```shellscript
docker build --tag sports_team_logos_crawler .
```


```shellscript
docker run --rm `
    --volume c:\\temp\\output:/output --volume c:\\temp\\tasks:/tasks:ro `
    --env http_proxy=$env:http_proxy --env https_proxy=$env:https_proxy `
    sports_team_logos_crawler:latest football_russian_cup.json
```

## Отладка

```shellscript
docker run --rm -it sports_team_logos_crawler:latest bash
```
