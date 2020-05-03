import datetime
from datetime import datetime
from typing import Dict, Optional

from aiohttp import ClientSession

from core.db import DatabaseWrapper


class Weather:
    def __init__(self, db: DatabaseWrapper):
        self._client = ClientSession()
        self._db = db

    async def process_message(self, text: str) -> Dict[str, str]:
        date = self._parse_date_from_text(text)
        if date is None:
            # ToDo: написать норм сообщения
            return {"text": "Не смог распознать сообщение! Попросить погоду можно на сегодня или на завтра"}

        forecast = await self._db.get_forecast_by_date(date)
        if forecast is None:
            # ToDo: написать норм сообщения
            return {"text": "Не смог распознать сообщение! Попросить погоду можно на сегодня или на завтра"}

    @staticmethod
    def _parse_date_from_text(text: str) -> Optional[str]:
        current_date = datetime.today()
        if 'ceгодня' in text:
            timedelta = datetime.timedelta(days=0)
        elif 'завтра' in text:
            timedelta = datetime.timedelta(days=1)
        else:
            return None

        return (current_date + timedelta).strftime('%Y-%m-%d')

