#!/bin/bash
python manage.py collectstatic
web: gunicorn download.wsgi:application
