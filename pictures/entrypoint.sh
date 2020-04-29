#!/usr/bin/env sh

#python -u api.py
gunicorn --bind 0.0.0.0:30600 --workers 1 --threads 4 --access-logfile '-' --log-level debug api
