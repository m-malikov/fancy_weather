# Fancy Weather
Лучший сервис с погодой в Москве.

![deploy](https://github.com/inyutin/fancy_weather/workflows/deploy/badge.svg)
![tests](https://github.com/inyutin/fancy_weather/workflows/tests/badge.svg)

Воспользоваться сервисом можно через
- Сайт: http://194.67.113.84:8080  
![site_pic](https://imgur.com/hDQKKmW)
- Бот в телеграмме: @fancy_weather_bot  
![bot_pic](https://imgur.com/Q7MAVOO)

## Архитектура

![scheme](https://i.imgur.com/hGgbxqg.png)

Проект разбит на 5 микросервисов. `Core` отвечает за получение погоды и распознавание сообщений пользователя. Также он получает картинки и стихи из `pictures` и `poems`.
Картинки - это картины известных русских художников, они разделены на 5 коллекций, отвечающих настроению каждой погоды. 
Стихи дополняют прогноз русским колоритом. Прогноз отформатирован так, чтобы быть приятным пользователю

`Web-front` и `tg_bot` получают данные из `core`

Стоит упомянуть, что в каждом сервисе применялись Docker, docker-compose, pytest, mypy

## Демонстрация
#### Web-интерфейс
![preview](https://i.imgur.com/2sM5J4x.jpg)

#### Telegram bot
![preview](https://i.imgur.com/hKszpWD.png)

## Запуск
Достаточно выполнить команду `docker-compose up --build`

Тесты: `py.test -vl {название модуля}`

Проверка кодстайла mypy: `mypy -p {название модуля}`
