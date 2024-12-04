#!/bin/bash
python manage.py collectstatic --noinput
web: gunicorn download.wsgi:application
