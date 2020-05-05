import os
from typing import Dict

import pytest

from lib.db import Forecast, DatabaseWrapper

DB_NAME = "test_weather"


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


@pytest.mark.freeze_time('2020-05-05 10:00:00')
def test_forecast_current_temperature():
    forecast = get_base_forecast()
    assert (20, 21) == forecast.current_temperature  # temp, feels_like


@pytest.mark.parametrize(
    "ten_hour, result_message",
    [
        ({
            'temp': 20,
            'feels_like': 21
        }, "+20 градусов Цельсия. Ощущается как +21. Ясно."),
        ({
             'temp': -10,
             'feels_like': -13
         }, "-10 градусов Цельсия. Ощущается как -13. Ясно.")
    ],
)
@pytest.mark.freeze_time('2020-05-05 10:00:00')
def test_forecast_description_hours(ten_hour, result_message):
    forecast = get_base_forecast()
    forecast.hours['10'] = ten_hour
    assert result_message == forecast.description  # temp, feels_like


@pytest.mark.parametrize(
    "condition, result_message",
    [
        ('cloudy', "+20 градусов Цельсия. Ощущается как +21. Облачно с прояснениями."),
        ("overcast", "+20 градусов Цельсия. Ощущается как +21. Пасмурно."),
    ],
)
@pytest.mark.freeze_time('2020-05-05 10:00:00')
def test_forecast_description_condition(condition, result_message):
    forecast = get_base_forecast()
    forecast.condition = condition
    assert result_message == forecast.description


@pytest.mark.asyncio
@pytest.mark.freeze_time('2020-05-05 10:00:00')
async def test_database_wrapper_just_insert():
    db_wrapper = DatabaseWrapper(db_uri=f'sqlite:///{DB_NAME}')  # Create db for tests
    await db_wrapper.init()

    await db_wrapper.insert_forecasts('clear', 'spring', [{
        'date': '2020-05-05',
        'sunrise': '04:00',
        'sunset': '20:00',
        'set_end': '21:00',
        'hours': [{'hour': '10', 'temp': 20, 'feels_like': 21}]
    }])

    forecast = await db_wrapper.get_forecast_by_date('2020-05-05')

    assert forecast.date == '2020-05-05'
    assert forecast.condition == 'clear'
    assert forecast.current_temperature == (20, 21)
    assert forecast.date == '2020-05-05'
    assert forecast.description == '+20 градусов Цельсия. Ощущается как +21. Ясно.'
    assert forecast.hours == {'10': {'temp': 20, 'feels_like': 21}}
    assert forecast.season == 'spring'
    assert forecast.set_end == '21:00'
    assert forecast.sunrise == '04:00'
    assert forecast.sunset == '20:00'

    os.remove(DB_NAME)


@pytest.mark.asyncio
@pytest.mark.freeze_time('2020-05-05 10:00:00')
async def test_database_wrapper_rewrite():
    db_wrapper = DatabaseWrapper(db_uri=f'sqlite:///{DB_NAME}')  # Create db for tests
    await db_wrapper.init()

    await db_wrapper.insert_forecasts('clear', 'spring', [{
        'date': '2020-05-05',
        'sunrise': '04:00',
        'sunset': '20:00',
        'set_end': '21:00',
        'hours': [{'hour': '10', 'temp': 20, 'feels_like': 21}]
    }])

    await db_wrapper.insert_forecasts('cloudy', 'winter', [{
        'date': '2020-05-05',
        'sunrise': '05:00',
        'sunset': '21:00',
        'set_end': '22:00',
        'hours': [{'hour': '10', 'temp': 21, 'feels_like': 22}]
    }])

    forecast = await db_wrapper.get_forecast_by_date('2020-05-05')

    assert forecast.date == '2020-05-05'
    assert forecast.condition == 'cloudy'
    assert forecast.current_temperature == (21, 22)
    assert forecast.date == '2020-05-05'
    assert forecast.description == '+21 градусов Цельсия. Ощущается как +22. Облачно с прояснениями.'
    assert forecast.hours == {'10': {'temp': 21, 'feels_like': 22}}
    assert forecast.season == 'winter'
    assert forecast.set_end == '22:00'
    assert forecast.sunrise == '05:00'
    assert forecast.sunset == '21:00'

    os.remove(DB_NAME)
