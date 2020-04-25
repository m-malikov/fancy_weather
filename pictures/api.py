import logging

from flask import Flask, request, send_file
from gevent import pywsgi

from generator import generate_picture

app = Flask('pictures')


@app.route('/generate/picture')
def generate_picture_api():
    """
    Accepts following weather types:
        rainy
        snowy
        cold
        warm
        spring
        autumn

    :return: picture bytes
    """
    logger = logging.getLogger('pictures')

    weather = request.args.get('weather')
    logger.error(f'Weather: {weather}')

    # byte_file = generate_picture(weather)
    # response = make_response(byte_file)
    # response.headers['Content-Type'] = 'image/jpg'
    file_path = generate_picture(weather)
    logger.error(f'Got file: {file_path}')
    if file_path is not None:
        return send_file(file_path), 200
    else:
        return None, 404


if __name__ == '__main__':
    port = int(os.getenv('PICTURES_PORT', 30600))

    logger = logging.getLogger('pictures')
    logger.error(f'Start on 0.0.0.0:{port}')  # f*ck gevent and use logger.error

    # app.run(host='0.0.0.0', port=port, debug=False)
    server = pywsgi.WSGIServer(('0.0.0.0', port), app, log=logger)
    server.serve_forever()
