import asyncio
from argparse import ArgumentParser
from typing import Dict

from aiohttp import ClientSession

from core.db import DatabaseWrapper

# Yandex api to Moscow forecast
API_URL = "https://api.weather.yandex.ru/v1/forecast?lat=55.75396&lon=37.620393&extra=true"


async def main(key: str, db_uri) -> None:
    db_wrapper = DatabaseWrapper(db_uri)

    headers: Dict[str, str] = {"X-Yandex-API-Key": key}
    async with ClientSession() as session:
        async with session.get(API_URL, headers=headers) as response:
            json_response = await response.json()
            forecasts = json_response['forecasts']
            db_wrapper.insert_forecasts(forecasts)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--key", required=True, help="key to yandex weather api")
    parser.add_argument("--db_uri", required=True, help="uri to db")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.key, args.db_uri))
