import logging
import os
from typing import Any

from flask import Flask, request, send_file

from generator import generate_picture

application = Flask('pictures')
gunicorn_logger = logging.getLogger('gunicorn.error')
application.logger.handlers = gunicorn_logger.handlers
application.logger.setLevel(gunicorn_logger.level)


@application.route('/generate/picture')
def generate_picture_api() -> Any:
    """
    Accepts following weather types:
        rainy
        snowy
        cold
        warm
        spring
        autumn

    Available at: http://localhost:30600/generate/picture?weather=warm

    :return: picture bytes
    """
    weather = request.args.get('weather')
    application.logger.info(f'Weather: {weather}')

    file_path = generate_picture(weather)
    if file_path is not None:
        application.logger.info(f'Got file: {file_path}')
        return send_file(file_path), 200
    else:
        application.logger.error(f'File for this weather type not found')
        return None, 404


if __name__ == '__main__':
    port = int(os.getenv('PICTURES_PORT', 30600))

    application.run(host='0.0.0.0', port=port, debug=False)
