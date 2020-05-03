#!/usr/bin/env sh

gunicorn --bind 0.0.0.0:30601 --workers 1 --threads 4 --access-logfile '-' --log-level debug poems.poems
