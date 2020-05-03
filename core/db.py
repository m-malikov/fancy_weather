import json
from typing import Any, List, Dict

from sqlalchemy import create_engine, Column, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather'

    date = Column('date', Text, primary_key=True)  # F.E. "2020-05-03"
    sunrise = Column('sunrise', Text)  # F.E. "04:41"
    sunset = Column('sunset', Text)  # F.E. "20:12"
    set_end = Column('set_end', Text)  # F.E. "20:57"
    hours = Column('hours', Text)  # Serialized data, F.E {'00': {'temp': 12, 'feels_like': 9}} 


class DatabaseWrapper:
    def __init__(self, db_uri: str) -> None:
        # The echo flag is a shortcut to setting up SQLAlchemy logging,
        # which is accomplished via Python’s standard logging module.
        engine = create_engine(db_uri, echo=True)

        self._session = sessionmaker(bind=engine)()
        Base.metadata.create_all(engine)

    def insert_forecasts(self, forecasts: List[Dict[str, Any]]) -> None:
        for forecast in forecasts:
            weather = Weather(
                date=forecast['date'],
                sunrise=forecast.get('sunrise', ''),
                sunset=forecast.get('sunset', ''),
                set_end=forecast.get('set_end', ''),
                hours=self._serialize_hours(forecast['hours'])
            )
            self._session.add(weather)

    @staticmethod
    def _serialize_hours(hours: List[Dict[str, Any]]) -> str:
        clear_hours: Dict[str, Dict[str, str]] = {}
        for hour in hours:
            clear_hours[hour['hour']] = {
                'temp': hour['temp'],
                'feels_like': hour['feels_like']
            }

        return json.dumps(clear_hours)

