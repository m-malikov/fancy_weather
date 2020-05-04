#!/usr/bin/env sh

flask init-db --datafile poems/poems_by_type.json &&
gunicorn --bind 0.0.0.0:30601 --workers 1 --threads 4 --access-logfile '-' --log-level info 'poems:create_app()'
