import asyncio
import json
import logging.config
from argparse import ArgumentParser
from typing import Dict

from aiohttp import ClientSession, web
from tornado.options import options

from core import define_options, api
from core.db import DatabaseWrapper
from core.weather import Weather

log = logging.getLogger(__name__)


async def update_weather(db: DatabaseWrapper) -> None:
    """
    Task to update weather from api every options.weather_update_interval seconds
    """
    headers: Dict[str, str] = {"X-Yandex-API-Key": options.yandex_api_key}
    while True:
        try:
            async with ClientSession() as session:
                async with session.get(options.yandex_api_url, headers=headers) as response:
                    json_response = await response.json()
                    log.info(f"Response from ya.api: {json_response}")  # We check api rarely, but it's important

                    condition = json_response['fact']['condition']
                    season = json_response['fact']['season']
                    forecasts = json_response['forecasts']
                    await db.insert_forecasts(condition, season, forecasts)
        except:
            # ToDo: add metrics
            log.exception("While updating Ya.Weather api en error occurred")
            await asyncio.sleep(60)  # Sleep short time in cause of error
        else:
            await asyncio.sleep(options.weather_update_interval)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config", required=True, help="path to service config file")
    args = parser.parse_args()

    # Define and parse all options as tornado options
    define_options.init(args.config)

    # Set logging
    with open(options.log_config_path) as f:
        log_config_path = json.load(f)
    logging.config.dictConfig(log_config_path)

    event_loop = asyncio.get_event_loop()

    # Init db
    db_wrapper = DatabaseWrapper(options.db_uri)
    event_loop.run_until_complete(db_wrapper.init())
    event_loop.create_task(update_weather(db_wrapper))  # Start updating forecasts

    weather = Weather(db_wrapper)

    api_app = api.create_app(weather)
    web.run_app(api_app, host=options.host, port=options.port)
