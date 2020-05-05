from typing import Optional, Dict

import pytest

from lib.db import Forecast
from lib.enums import Condition, WeatherType, Season
from lib.weather import Weather


def get_base_hours() -> Dict[str, Dict[str, float]]:
    return {
        str(hour): {
            'temp': 2*hour,
            'feels_like': 2*hour + 1}
        for hour in range(0, 25)
    }


def get_base_forecast() -> Forecast:
    return Forecast(
        date='2020-05-05',
        condition='clear',
        season='spring',
        sunrise='04:00',
        sunset='20:00',
        set_end='21:00',
        hours=get_base_hours()
    )


class MockDatabaseWrapper:
    def __init__(self):
        return

    @staticmethod
    async def get_forecast_by_date(date: str) -> Optional[Forecast]:
        if date == '2020-05-05':
            return get_base_forecast()

        return None


@pytest.mark.parametrize(
    "messages, result",
    [
        (['Сегодня', 'Какая погода сегодня?', 'Погода сегодня?'], "2020-05-05"),
        (['Завтра', 'Какая погода завтра?', 'Погода завтра?', 'погода через один день', 'через 1 день'], "2020-05-06"),
        (['послезавтра', 'Какая погода послезавтра?', 'Погода послезавтра?', 'через 2 дня'], "2020-05-07"),
        (['через 3 дня', 'через три дня'], "2020-05-08"),
        (['Через 4 дня', 'через четыре дня'], "2020-05-09"),
        (['Через 5 дней', 'через пять дней'], "2020-05-10"),
        (['Черещ 6 дней', 'Погода через шесть дней'], "2020-05-11"),
        (['Погода через неделю', 'На месяц вперёд'], None),
    ],
)
@pytest.mark.freeze_time('2020-05-05 10:00:00')
def test_parse_date_from_text(messages, result):
    for message in messages:
        assert result == Weather._parse_date_from_text(text=message)


@pytest.mark.asyncio
@pytest.mark.freeze_time('2020-05-05 10:00:00')
async def test_weather_date_is_none():
    db_wrapper = MockDatabaseWrapper()
    weather = Weather(db_wrapper)

    message = await weather.process_message("Погода")
    assert message == {
        "desc": None,
        "text": "Не смог распознать сообщение! Погоду можно узнать только на ближайшую неделю.",
        "author": None,
        "picture": None
    }


@pytest.mark.asyncio
@pytest.mark.freeze_time('2020-05-05 10:00:00')
async def test_weather_no_forecast():
    db_wrapper = MockDatabaseWrapper()
    weather = Weather(db_wrapper)

    message = await weather.process_message("завтра")
    assert message == {
        "desc": None,
        "text": "К сожалению, у меня нет данных о погоде на 2020-05-06",
        "author": None,
        "picture": None
    }


@pytest.mark.freeze_time('2020-05-05 10:00:00')
def test_weather_parse_forecast_to_weather_type():
    forecast = get_base_forecast()

    forecast.condition = Condition.CLOUDY_AND_RAIN
    assert WeatherType.RAINY == Weather._parse_forecast_to_weather_type(forecast)

    forecast.condition = Condition.CLOUDY_AND_LIGHT_SNOW
    assert WeatherType.SNOWY == Weather._parse_forecast_to_weather_type(forecast)

    forecast.condition = Condition.CLEAR

    forecast.season = Season.SPRING
    assert WeatherType.SPRING == Weather._parse_forecast_to_weather_type(forecast)

    forecast.season = Season.AUTUMN
    assert WeatherType.AUTUMN == Weather._parse_forecast_to_weather_type(forecast)

    forecast.season = Season.WINTER
    assert WeatherType.WARM == Weather._parse_forecast_to_weather_type(forecast)

    forecast.hours['10'] = {
        'temp': 5,
        'feels_like': 3
    }
    assert WeatherType.COLD == Weather._parse_forecast_to_weather_type(forecast)
