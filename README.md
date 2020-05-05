# Fancy Weather
Лучший сервис с погодой в Москве

![deploy](https://github.com/inyutin/fancy_weather/workflows/deploy/badge.svg)
![tests](https://github.com/inyutin/fancy_weather/workflows/tests/badge.svg)

## Архитектура

![scheme](https://i.imgur.com/hGgbxqg.png)

Также в каждом сервисе применялись Docker, docker-compose, pytest, mypy

## Демонстрация
#### Web-интерфейс
![preview](https://i.imgur.com/2sM5J4x.jpg)

#### Telegram bot
![preview](https://i.imgur.com/hKszpWD.png)

## Запуск
Достаточно выполнить команду `docker-compose up --build`

Тесты: `py.test -vl {название модуля}`

Проверка кодстайла mypy: `mypy -p {название модуля}`
