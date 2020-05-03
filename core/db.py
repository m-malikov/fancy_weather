import json
from typing import Any, List, Dict

from sqlalchemy.orm import mapper
from sqlalchemy.sql.ddl import CreateTable
from sqlalchemy_aio import ASYNCIO_STRATEGY
from sqlalchemy import create_engine, Column, Text, Table, MetaData


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
            Column('sunrise', Text),  # F.E. "04:41"
            Column('sunset', Text),  # F.E. "20:12"
            Column('set_end', Text),  # F.E. "20:57"
            Column('hours', Text),  # Serialized data, F.E {'00': {'temp': 12, 'feels_like': 9}}
        )

    async def init(self) -> None:
        if not self._engine.dialect.has_table(self._engine.sync_engine, "weather"):
            await self._engine.execute(CreateTable(self._table))

    async def insert_forecasts(self, forecasts: List[Dict[str, Any]]) -> None:
        """
        Update or insert forecasts in db.
        This method quite ineffective, we update rows one by one.
        Look here why we cant implement insert on conflict: https://github.com/sqlalchemy/sqlalchemy/issues/4010

        However, it's okay for us. len(forecasts) no more that 7 and we update forecasts rarely
        :param forecasts: list of forecasts to update in db
        """
        conn = await self._engine.connect()
        for forecast in forecasts:
            value = {
                'sunrise': forecast.get('sunrise', ''),
                'sunset': forecast.get('sunset', ''),
                'set_end': forecast.get('set_end', ''),
                'hours': self._serialize_hours(forecast.get('hours', [])),
            }
            old_forecast_select = await conn.execute(self._table.select(self._table.c.date == forecast['date']))
            old_forecast = await old_forecast_select.fetchall()
            if len(old_forecast) > 0:
                await conn.execute(self._table.update().where(self._table.c.date == forecast['date']).values(value))
            else:
                value['date'] = forecast['date']
                await conn.execute(self._table.insert().values(value))

    @staticmethod
    def _serialize_hours(hours: List[Dict[str, Any]]) -> str:
        clear_hours: Dict[str, Dict[str, str]] = {}
        for hour in hours:
            clear_hours[hour['hour']] = {
                'temp': hour['temp'],
                'feels_like': hour['feels_like']
            }

        return json.dumps(clear_hours)

