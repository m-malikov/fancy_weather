import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

from aiohttp import ClientSession, ClientResponseError
from tornado.options import options

from core.db import DatabaseWrapper, Forecast
from core.enums import WeatherType, Condition, Season


log = logging.getLogger(__name__)


class Weather:
    """
    Main class for handling users messages.
    This class parse them, choose weather type, fetch picture and poem and send them back.
    """
    def __init__(self, db: DatabaseWrapper):
        self._client = ClientSession()
        self._db = db

    async def process_message(self, text: str) -> Dict[str, Optional[str]]:
        date = self._parse_date_from_text(text)
        if date is None:
            text = "Не смог распознать сообщение! Погоду можно узнать только на близжайшую неделю."
            return {"text": text, "picture": None}

        forecast = await self._db.get_forecast_by_date(date)
        if forecast is None:
            text = f"К сожалению, у меня нет данных о погоде на {date}"
            return {"text": text, "picture": None}

        weather_type = self._parse_forecast_to_weather_type(forecast).value

        text = await self._fetch_poem(weather_type)
        picture = await self._fetch_picture(weather_type)
        return {"text": text, "picture": picture}

    @staticmethod
    def _parse_date_from_text(text: str) -> Optional[str]:
        current_date = datetime.today()
        if 'сегодня' in text:
            time_delta = timedelta(days=0)
        elif 'завтра' in text or "1 день" in text or "один день" in text:
            time_delta = timedelta(days=1)
        elif 'послезавтра' in text or "2 дня" in text or "два дня" in text:
            time_delta = timedelta(days=2)
        elif "3 дня" in text or "три дня" in text:
            time_delta = timedelta(days=3)
        elif "4 дня" in text or "четыре дня" in text:
            time_delta = timedelta(days=4)
        elif "5 дней" in text or "пять дней" in text:
            time_delta = timedelta(days=5)
        elif '6 дней' in text or "6 дней" in text:
            time_delta = timedelta(days=6)
        elif 'неделю' in text or "7 дней" in text or "семь дней" in text:
            time_delta = timedelta(days=7)
        else:
            return None

        return (current_date + time_delta).strftime('%Y-%m-%d')

    @staticmethod
    def _parse_forecast_to_weather_type(forecast: Forecast) -> WeatherType:
        condition = Condition(forecast.condition)
        season = Season(forecast.season)

        if condition in Condition.RAIN_CONDITIONS.value:
            return WeatherType.RAINY

        if condition in Condition.SNOWY_CONDITIONS.value:
            return WeatherType.SNOWY

        if season == Season.spring:
            return WeatherType.SPRING

        if season == Season.AUTUMN:
            return WeatherType.AUTUMN

        average_temperature = sum([hour['temp'] for hour in forecast.hours.values()]) / len(forecast.hours)
        if average_temperature > 10.0:
            return WeatherType.WARM

        return WeatherType.COLD

    async def _fetch_poem(self, weather_type: str) -> Optional[str]:
        poems_api = f"http://{options.poems_host}:{options.poems_port}{options.poems_api}{weather_type}"
        try:
            async with self._client.get(poems_api) as poems:
                poems = await poems.json()
                return poems['text']
        except (ClientResponseError, json.JSONDecodeError) as e:
            # ToDo: add metrics
            log.exception(f"While fetching pictures an error occured: {str(e.args)}")

        return None

    async def _fetch_picture(self, weather_type: str) -> Optional[str]:
        picture_api = f"http://{options.pictures_host}:{options.pictures_port}{options.pictures_api}{weather_type}"
        try:
            async with self._client.get(picture_api) as picture_request:
                picture_json = await picture_request.json()
                if not picture_json.get('error', ''):
                    return picture_json['data']
        except (ClientResponseError, json.JSONDecodeError) as e:
            # ToDo: add metrics
            log.exception(f"While fetching pictures an error occured: {str(e.args)}")

        return None
