from typing import Any, Dict, List

from flask import current_app as application
from flask import request

from pictures.generator import generate_picture


def generate_picture_api(images_links: Dict[str, List[str]]) -> Any:
    """
    Accepts following weather types:
        rainy
        snowy
        cold
        warm
        spring
        autumn

    Available at: http://localhost:30600/generate/picture?weather=warm

    :return: picture link
    """
    weather = request.args['weather']
    application.logger.info(f'Weather: {weather}')

    image_link = generate_picture(weather, images_links)
    if image_link is not None:
        application.logger.info(f'Got link: {image_link}')
        return {'data': image_link, 'error': ''}, 200
    else:
        err_msg = 'File for this weather type not found'
        application.logger.error(err_msg)
        return {'data': '', 'error': err_msg}, 404
