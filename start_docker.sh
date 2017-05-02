#!/bin/bash
python manage.py collectstatic --noinput
gunicorn --bind unix:/ihc-image-analysis/lap.sock lap.wsgi:application &
nginx -g "daemon off;"