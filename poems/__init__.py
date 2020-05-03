import os

from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
import logging
import click
import json
from typing import Dict, Optional, List

db = SQLAlchemy()


def create_app(test_config: Optional[Dict[str, str]] = None) -> Flask:
    app = Flask("poems")
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.cli.add_command(init_db_command)

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers

    from poems import handlers
    app.route("/")(handlers.get_poem)
    return app


def init_db(data: List[Dict["str", "str"]] = []) -> None:
    db.drop_all()
    db.create_all()
    from poems.models import Poem
    for item in data:
        db.session.add(Poem(
            weather_type=item["type"],
            text=item["text"],
            info=item["info"])
        )
    db.session.commit()


@click.command("init-db")
@click.option("--datafile", default=None,
              help="File with poems to fill database")
@with_appcontext
def init_db_command(datafile: str) -> None:
    if datafile:
        with open(datafile, "r") as f:
            data = json.loads(f.read())["poems"]
    else:
        data = []
    init_db(data)
    click.echo("Initialized the database.")
