import os
import sys
import json
import logging.config
from argparse import ArgumentParser

import aiohttp
import tornado.options
from tornado.options import options, parse_config_file
from aiogram import Bot, Dispatcher, executor, types

log = logging.getLogger(__name__)


def define_tornado_options() -> None:
    """
    Just define tornado options
    """
    tornado.options.define("log_config_path", help="path to log_config", type=str, default="logging.json")
    tornado.options.define("core_host", help="hostname to core", type=str, default="0.0.0.0")
    tornado.options.define("core_port", help="hostname to core", type=str, default="5000")
    tornado.options.define("core_api", help="hostname to core", type=str, default="/api/v1/weather?text=")


async def send_welcome(message: types.Message) -> None:
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    text = "Привет! Я бот, который поможет узнать погоду в Москве. \n" \
           "Спроси *Какая погода сегодня*?."
    await message.reply(text, parse_mode="Markdown")


async def get_weather(message: types.Message) -> None:
    """
    This handler response to all other request.
    """
    url = f"http://{options.core_host}:{options.core_port}{options.core_api}{message.text}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                json_response = await response.json()
    except Exception as e:
        log.exception(f"While requesting core an error occurred {str(e.args)}")

    text, author = json_response.get('text'), json_response.get('author')
    desc, picture = json_response.get('desc'), json_response.get('picture')

    if desc:
        await message.answer(desc, parse_mode="Markdown")

    if text:
        await message.answer(text, parse_mode="Markdown")

    if author:
        await message.answer(author, parse_mode="Markdown")

    if picture:
        await message.answer_photo(picture)

if __name__ == "__main__":
    TG_TOKEN = os.environ.get("TG_TOKEN")
    if not TG_TOKEN:
        sys.exit("Set environment variable TG_TOKEN")

    parser = ArgumentParser()
    parser.add_argument("--config", help="path to config file")
    args = parser.parse_args()

    define_tornado_options()

    if args.config is not None:
        parse_config_file(args.config)

    with open(options.log_config_path) as f:
        log_config = json.load(f)
    logging.config.dictConfig(log_config)

    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher(bot)

    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(get_weather)

    executor.start_polling(dp, skip_updates=True)
