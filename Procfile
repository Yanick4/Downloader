#!/bin/bash
release: python manage.py collectstatic --noinput
web: gunicorn download.wsgi:application
