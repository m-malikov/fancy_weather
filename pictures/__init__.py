import json
import logging
import os
from functools import partial, update_wrapper
from typing import Dict, List

import requests
from flask import Flask

from pictures.generator import WeatherToImgurAlbum, generate_picture


def create_app() -> Flask:
    application = Flask('pictures')
    gunicorn_logger = logging.getLogger('gunicorn.error')
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)

    images_links = init_available_images_collection(application)

    from pictures import api
    generate_picture_api = partial(api.generate_picture_api, images_links)
    update_wrapper(generate_picture_api, api.generate_picture_api)
    application.route('/generate/picture')(generate_picture_api)

    return application


def init_available_images_collection(application: Flask) \
        -> Dict[str, List[str]]:
    images_links = {}
    imgur_client = os.getenv('IMGUR_CLIENT')
    for weather_type in WeatherToImgurAlbum:
        application.logger.info(
            f'Getting {weather_type.value} collection for {weather_type}'
        )

        url = f'https://api.imgur.com/3/album/{weather_type.value}/images'

        headers = {
            'Authorization': f'Client-ID {imgur_client}'
        }

        try:
            response = requests.request('GET', url,
                                        headers=headers, data={}, files={})
        except Exception as e:
            application.logger.error(f'Error getting album images: {repr(e)}')
            raise

        try:
            images = json.loads(response.text)['data']
        except Exception as e:
            application.logger.error(f'Error parsing response: {repr(e)}')
            raise

        links = [image['link'] for image in images]
        if len(links) != 0:
            images_links[weather_type.value] = links
        else:
            application.logger.error(
                f'Got empty collection for {weather_type}'
            )
            raise Exception(
                f'Got empty collection for {weather_type}'
            )
    return images_links


if __name__ == '__main__':
    port = int(os.getenv('PICTURES_PORT', 30600))

    application = create_app()
    application.run(host='0.0.0.0', port=port, debug=False)
