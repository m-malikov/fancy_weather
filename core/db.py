import json
from dataclasses import dataclass
from typing import Any, List, Dict, Optional

from sqlalchemy.sql.ddl import CreateTable, DropTable
from sqlalchemy_aio import ASYNCIO_STRATEGY
from sqlalchemy import create_engine, Column, Text, Table, MetaData


@dataclass
class Forecast:
    """
    Representation of forecast to return for simpler usage
    """
    date: str
    condition: str
    season: str
    sunrise: str
    sunset: str
    set_end: str
    hours: Dict[str, Dict[str, float]]


class DatabaseWrapper:
    _TABLE_NAME = "weather"

    def __init__(self, db_uri: str) -> None:
        # The echo flag is a shortcut to setting up SQLAlchemy logging,
        # which is accomplished via Python’s standard logging module.
        self._engine = create_engine(db_uri, echo=True, strategy=ASYNCIO_STRATEGY)

        metadata = MetaData()
        self._table = Table(
            self._TABLE_NAME, metadata,
            Column('date', Text, primary_key=True),  # F.E. "2020-05-03"
            Column('condition', Text),  # F.E. "overcast"
            Column('season', Text),  # F.E. "season"
            Column('sunrise', Text),  # F.E. "04:41"
            Column('sunset', Text),  # F.E. "20:12"
            Column('set_end', Text),  # F.E. "20:57"
            Column('hours', Text),  # Serialized data, F.E {'00': {'temp': 12, 'feels_like': 9}}
        )

    async def init(self) -> None:
        if not self._engine.dialect.has_table(self._engine.sync_engine, "weather"):
            await self._engine.execute(CreateTable(self._table))

    async def insert_forecasts(self, condition: str, season: str, forecasts: List[Dict[str, Any]]) -> None:
        """
        Update or insert forecasts in db.
        This method quite ineffective, we update rows one by one.
        Look here why we cant implement insert on conflict: https://github.com/sqlalchemy/sqlalchemy/issues/4010

        However, it's okay for us. len(forecasts) no more that 7 and we update forecasts rarely
        :param condition:
        :param forecasts: list of forecasts to update in db
        """
        conn = await self._engine.connect()
        for forecast in forecasts:
            value = {
                'date': forecast['date'],
                'condition': condition,
                'season': season,
                'sunrise': forecast.get('sunrise', ''),
                'sunset': forecast.get('sunset', ''),
                'set_end': forecast.get('set_end', ''),
                'hours': self._serialize_hours(forecast.get('hours', [])),
            }
            old_forecast_select = await conn.execute(self._table.select(self._table.c.date == forecast['date']))
            old_forecast = await old_forecast_select.fetchone()
            if old_forecast:
                await conn.execute(self._table.update().where(self._table.c.date == forecast['date']).values(value))
            else:
                await conn.execute(self._table.insert().values(value))

        await conn.close()

    async def get_forecast_by_date(self, date: str) -> Optional[Forecast]:
        """
        :param date: string of date that looks like "year-month-day"
        :return: row as dict
        """
        conn = await self._engine.connect()
        forecast_select = await conn.execute(self._table.select(self._table.c.date == date))
        forecast = await forecast_select.fetchone()
        await conn.close()

        if forecast is None:
            return None

        return Forecast(
            date=forecast.date,
            condition=forecast.condition,
            season=forecast.season,
            sunrise=forecast.sunrise,
            sunset=forecast.sunset,
            set_end=forecast.set_end,
            hours=json.loads(forecast.hours),
        )

    @staticmethod
    def _serialize_hours(hours: List[Dict[str, Any]]) -> str:
        clear_hours: Dict[str, Dict[str, str]] = {}
        for hour in hours:
            clear_hours[hour['hour']] = {
                'temp': hour['temp'],
                'feels_like': hour['feels_like']
            }

        return json.dumps(clear_hours)

