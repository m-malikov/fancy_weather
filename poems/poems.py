import logging
import os
from typing import Any

from flask import Flask, request, jsonify

from poems.poem_finder import PoemFinder

poem_finder = PoemFinder('poems/poems_by_type.json')

app = Flask('poems')
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

application = app


@app.route('/')
def get_poem() -> Any:
    """
    Responds to poem requests using poem finder.
    Weather type is passed in `weather` uri param.
    :return: json with poem or 404 and empty body in case
    weather type is not found
    """
    weather = request.args.get('weather')
    app.logger.info('Weather: {}'.format(weather))

    poem_data = poem_finder.get_poem(weather)
    if poem_data is not None:
        app.logger.info('Poem found: {}'.format(poem_data["info"]))
        return jsonify(poem_data), 200
    else:
        app.logger.error('Unknown weather type: {}'.format(weather))
        return "", 404


if __name__ == '__main__':
    port = int(os.getenv('POEMS_PORT', 30601))
    app.run(host='0.0.0.0', port=port, debug=False)
