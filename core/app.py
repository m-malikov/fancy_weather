import asyncio
from argparse import ArgumentParser
from typing import Dict

from aiohttp import ClientSession, web
from tornado.options import options

from core import define_options, api
from core.db import DatabaseWrapper


async def update_weather(db: DatabaseWrapper) -> None:
    """
    Task to update weather from api every options.weather_update_interval seconds
    """
    while True:
        headers: Dict[str, str] = {"X-Yandex-API-Key": options.yandex_api_key}
        async with ClientSession() as session:
            async with session.get(options.yandex_api_url, headers=headers) as response:
                json_response = await response.json()
                forecasts = json_response['forecasts']
                await db.insert_forecasts(forecasts)
        await asyncio.sleep(options.weather_update_interval)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config", required=True, help="path to service config file")
    args = parser.parse_args()

    # Define and parse all options as tornado options
    define_options.init(args.config)

    event_loop = asyncio.get_event_loop()

    db_wrapper = DatabaseWrapper(options.db_uri)
    event_loop.run_until_complete(db_wrapper.init())
    event_loop.create_task(update_weather(db_wrapper))  # Start updating weather task

    api_app = api.create_app()
    web.run_app(api_app, host=options.host, port=options.port)
