from flask import request, Response, jsonify
from sqlalchemy import func

from poems.models import Poem


def get_poem() -> Response:
    """
    Responds to poem requests using poem finder.
    Weather type is passed in `weather` uri param.
    :return: json with poem or 404 and empty body in case
    weather type is not found
    """
    weather = request.args['weather']

    poem_object = Poem.query.filter_by(weather_type=weather)\
                      .order_by(func.random())\
                      .limit(1).one_or_none()
    if poem_object is not None:
        return jsonify({
            "text": poem_object.text,
            "info": poem_object.info
        })
    else:
        return Response("", 404)
