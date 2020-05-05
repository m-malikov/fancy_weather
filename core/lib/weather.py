import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from aiohttp import ClientSession, ClientResponseError
from tornado.options import options

from lib.db import DatabaseWrapper, Forecast
from lib.enums import WeatherType, Condition, Season


log = logging.getLogger(__name__)


class Weather:
    """
    Main class for handling users messages.
    This class parse them, choose weather type, fetch picture and poem and send them back.
    """
    def __init__(self, db: DatabaseWrapper):
        self._client = ClientSession()
        self._db = db

    async def process_message(self, message: str) -> Dict[str, Optional[str]]:
        date = self._parse_date_from_text(message)

        if date is None:
            text: Optional[str] = "Не смог распознать сообщение! Погоду можно узнать только на ближайшую неделю."
            return {"desc": None, "text": text, "author": None, "picture": None}

        forecast = await self._db.get_forecast_by_date(date)
        if forecast is None:
            text = f"К сожалению, у меня нет данных о погоде на {date}"
            return {"desc": None, "text": text, "author": None, "picture": None}

        desc = forecast.description
        weather_type = self._parse_forecast_to_weather_type(forecast).value

        text, author = await self._fetch_poem(weather_type)
        picture = await self._fetch_picture(weather_type)
        return {"desc": desc, "text": text, "author": author, "picture": picture}

    @staticmethod
    def _parse_date_from_text(text: str) -> Optional[str]:
        current_date = datetime.today()

        clear_text = text.lower()
        if 'сегодня' in clear_text:
            time_delta = timedelta(days=0)
        elif 'завтра' in clear_text or "1 день" in clear_text or "один день" in clear_text:
            time_delta = timedelta(days=1)
        elif 'послезавтра' in clear_text or "2 дня" in clear_text or "два дня" in clear_text:
            time_delta = timedelta(days=2)
        elif "3 дня" in clear_text or "три дня" in clear_text:
            time_delta = timedelta(days=3)
        elif "4 дня" in clear_text or "четыре дня" in clear_text:
            time_delta = timedelta(days=4)
        elif "5 дней" in clear_text or "пять дней" in clear_text:
            time_delta = timedelta(days=5)
        elif '6 дней' in clear_text or "6 дней" in clear_text:
            time_delta = timedelta(days=6)
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

        if forecast.current_temperature[0] > 10.0:
            return WeatherType.WARM

        return WeatherType.COLD

    async def _fetch_poem(self, weather_type: str) -> Tuple[Optional[str], Optional[str]]:
        poems_api = f"http://{options.poems_host}:{options.poems_port}{options.poems_api}{weather_type}"
        try:
            async with self._client.get(poems_api) as poems:
                poems_json = await poems.json()
                return poems_json['text'], poems_json['info']
        except (ClientResponseError, json.JSONDecodeError) as e:
            log.exception(f"While fetching pictures an error occured: {str(e.args)}")

        return None, None

    async def _fetch_picture(self, weather_type: str) -> Optional[str]:
        picture_api = f"http://{options.pictures_host}:{options.pictures_port}{options.pictures_api}{weather_type}"
        try:
            async with self._client.get(picture_api) as picture_request:
                picture_json = await picture_request.json()
                if not picture_json.get('error', ''):
                    return picture_json['data']
        except (ClientResponseError, json.JSONDecodeError) as e:
            log.exception(f"While fetching pictures an error occured: {str(e.args)}")

        return None
